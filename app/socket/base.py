import socketio


server_sio = socketio.AsyncServer(async_mode='asgi',
                                  cors_allowed_origins='*',
                                  namespaces='*',
                                  max_http_buffer_size=1024 * 1024 * 100)
