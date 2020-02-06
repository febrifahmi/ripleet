import pusher

pusher_client = pusher.Pusher(
  app_id='xxxxxx',
  key='xxxx',
  secret='xxxx',
  cluster='xxx',
  ssl=True
)

pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
