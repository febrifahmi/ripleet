import pusher

pusher_client = pusher.Pusher(
  app_id='771414',
  key='key',
  secret='secret',
  cluster='ap1',
  ssl=True
)

pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
