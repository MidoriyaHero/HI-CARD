import re

def is_valid_email(email):
  regex = r'^[a-z0-9.+_-]+@[a-z0-9.-]+\.[a-z]{2,}$'
  return bool(re.match(regex, email))

# Example usage
email = "rgerg"
if is_valid_email(email):
  print("Valid email address")
else:
  print("Invalid email address")
