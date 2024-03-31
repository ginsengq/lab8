import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Paint")
    
    radius = 15
    x = 0
    y = 0
    mode = 'blue'
    points = []
    drawing = False
    
    while True:
        
        pressed = pygame.key.get_pressed()
        
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
            
                # determine if a letter key was pressed 
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                elif event.key == pygame.K_l:
                    mode = 'rectangle'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left click grows radius 
                    if mode != 'circle' and mode != 'rectangle':
                        drawing = True
                    else:
                        x, y = event.pos
                elif event.button == 3: # right click shrinks radius
                    radius = max(1, radius - 1)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            
            if event.type == pygame.MOUSEMOTION:
                # if mouse moved, add point to list 
                if drawing:
                    position = event.pos
                    points.append(position)
                    points = points[-256:]
                
        screen.fill((0, 0, 0))
        
        # draw all points 
        i = 0
        while i < len(points) - 1:
            drawShapeBetween(screen, i, points[i], points[i + 1], radius, mode)
            i += 1
        
        pygame.display.flip()
        
        clock.tick(60)

def drawShapeBetween(screen, index, start, end, width, mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))
    
    if mode == 'blue':
        color = (c1, c1, c2)
    elif mode == 'red':
        color = (c2, c1, c1)
    elif mode == 'green':
        color = (c1, c2, c1)
    elif mode == 'circle' or mode == 'rectangle':
        color = (255, 255, 255)  # White for drawing shapes
    elif mode == 'eraser':
        color = (0, 0, 0)  # Black for erasing
    
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    if mode == 'circle':
        pygame.draw.circle(screen, color, (start[0], start[1]), width)
    elif mode == 'rectangle':
        pygame.draw.rect(screen, color, (start[0], start[1], end[0] - start[0], end[1] - start[1]))
    else:
        for i in range(iterations):
            progress = 1.0 * i / iterations
            aprogress = 1 - progress
            x = int(aprogress * start[0] + progress * end[0])
            y = int(aprogress * start[1] + progress * end[1])
            pygame.draw.circle(screen, color, (x, y), width)

main()

'''
'r' - red
'g' - green
'b' - blue
'c' - circle
'l' - rectangle
'e' - eraser
'ESC' - exit 
'''