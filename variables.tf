variable "NOTION_TOKEN" {
  description = "Token for Notion API"
  type        = string
  sensitive   = true
}

variable "NOTION_DATABASE_ID" {
  description = "Database ID for Notion"
  type        = string
  sensitive   = true
}

variable "OPENAI_API_KEY" {
  description = "API Key for OpenAI"
  type        = string
  sensitive   = true
}

variable "SENDER_EMAIL" {
  description = "Email address of the sender"
  type        = string
  sensitive   = true
}

variable "RECIPIENT_EMAIL_1" {
  description = "Email address of the recipient"
  type        = string
  sensitive   = true
}

variable "RECIPIENT_EMAIL_2" {
  description = "Email address of the recipient"
  type        = string
  sensitive   = true
}

