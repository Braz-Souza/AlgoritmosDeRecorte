def cohen_sutherland(p1, p2, clip_window):
    x_min, y_min, x_max, y_max = clip_window
    
    def get_region_code(x, y):
        code = [0, 0, 0, 0]
        
        if x < x_min:
            code[0] = 1
        elif x > x_max:
            code[1] = 1
            
        if y < y_min:
            code[2] = 1
        elif y > y_max:
            code[3] = 1
            
        return code
    
    x1, y1 = p1
    x2, y2 = p2
    
    while True:
        code1 = get_region_code(x1, y1)
        code2 = get_region_code(x2, y2)
        
        if code1 == [0, 0, 0, 0] and code2 == [0, 0, 0, 0]:
            return [x1, y1], [x2, y2]
        
        reject = False
        for i in range(4):
            if code1[i] == 1 and code2[i] == 1:
                reject = True
                break
        
        if reject:
            return None, None
        
        if code1 != [0, 0, 0, 0]:
            code_out = code1
            x_out, y_out = x1, y1
        else:
            code_out = code2
            x_out, y_out = x2, y2
        
        if code_out[0] == 1:
            x = x_min
            y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
        elif code_out[1] == 1:
            x = x_max
            y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
        elif code_out[2] == 1:
            y = y_min
            x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
        elif code_out[3] == 1:
            y = y_max
            x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
        
        if x_out == x1 and y_out == y1:
            x1, y1 = x, y
        else:
            x2, y2 = x, y