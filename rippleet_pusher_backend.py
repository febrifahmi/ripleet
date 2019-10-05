import pusher

pusher_client = pusher.Pusher(
  app_id='771414',
  key='0c212ccb1794305437ea',
  secret='21ee090206a92f96a757',
  cluster='ap1',
  ssl=True
)

pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
