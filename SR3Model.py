from gl import Render

r = Render()
r.glInit(680,880)

r.load('./goku.obj', (0.1, 0.05), (3200, 3200))

r.glFinish("goku.bmp")