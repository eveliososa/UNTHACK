import stripe

# Set your secret key: remember to switch to your live secret key in production
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

intent = stripe.PaymentIntent.create(
  amount=1099,
  currency='usd',
)