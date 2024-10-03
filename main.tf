data "archive_file" "coffee_lambda_zip" {
  type        = "zip"
  source_dir  = "./coffee_lambda/code"
  output_path = "coffee_lambda.zip"
}

resource "aws_iam_role" "coffee_lambda_role" {
  name = "coffee-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Effect = "Allow"
      Sid    = ""
    }]
  })
}

resource "aws_iam_policy" "coffee_lambda_policy" {
  name        = "coffee-lambda-policy"
  description = "Policy to allow Lambda function to push to Cloudwatch"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents", "ses:SendEmail", "ses:SendRawEmail"],
        Resource = "*",
        Effect   = "Allow"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "coffee_lambda_attachment" {
  policy_arn = aws_iam_policy.coffee_lambda_policy.arn
  role       = aws_iam_role.coffee_lambda_role.name
}

resource "aws_lambda_function" "coffee_lambda_function" {
  function_name = "coffee-lambda-function"
  role          = aws_iam_role.coffee_lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.10"
  timeout       = 60
  filename      = data.archive_file.coffee_lambda_zip.output_path
  layers = [aws_lambda_layer_version.my_layer.arn]
  publish = true
  environment {
    variables = {
      NOTION_TOKEN       = var.NOTION_TOKEN,
      NOTION_DATABASE_ID = var.NOTION_DATABASE_ID,
      OPENAI_API_KEY     = var.OPENAI_API_KEY,
      SENDER_EMAIL       = var.SENDER_EMAIL,
      RECIPIENT_EMAIL    = var.RECIPIENT_EMAIL
    }
  }
}

resource "aws_iam_role" "coffee_scheduler_role" {
  name = "coffee-scheduler-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Principal = {
        Service = "scheduler.amazonaws.com"
      }
      Effect = "Allow"
      Sid    = ""
      }
    ]
  })
}

resource "aws_iam_policy" "coffee_scheduler_policy" {
  name        = "schedule-policy"
  description = "Policy to allow AWS scheduler to invoke the coffee-lambda-function"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "lambda:InvokeFunction"
        Resource = aws_lambda_function.coffee_lambda_function.arn
        Effect   = "Allow"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "coffee_scheduler_attachment" {
  policy_arn = aws_iam_policy.coffee_scheduler_policy.arn
  role       = aws_iam_role.coffee_scheduler_role.name
}

resource "aws_scheduler_schedule" "coffee_scheduler" {
  name = "coffee-scheduler"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(0 0 11 * ? *)"

  target {
    arn      = aws_lambda_function.coffee_lambda_function.arn
    role_arn = aws_iam_role.coffee_scheduler_role.arn
  }
}

resource "null_resource" "install_dependencies" {
  provisioner "local-exec" {
    command = <<EOT
      pip install -r coffee_lambda/lambda_layer/requirements.txt -t coffee_lambda/lambda_layer/python/ --implementation cp --python-version 3.10 --only-binary=:all:
      cd coffee_lambda/lambda_layer && zip -r ./lambda_layer.zip .
    EOT
  }

  triggers = {
    always_run = "${timestamp()}"
  }
}

resource "aws_lambda_layer_version" "my_layer" {

  depends_on = [ null_resource.install_dependencies ]

  layer_name  = "coffee-lambda-libs"
  description = "A layer containing requests, openai, notion_client, and exceptiongroup"

  compatible_runtimes = ["python3.10"] 
  filename            = "coffee_lambda/lambda_layer/lambda_layer.zip"
}
