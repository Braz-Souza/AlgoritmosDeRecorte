def sutherland_hodgman(polygon, clip_window):
    x_min, y_min, x_max, y_max = clip_window
    
    def inside(p, edge):
        if edge == 'left':
            return p[0] >= x_min
        elif edge == 'right':
            return p[0] <= x_max
        elif edge == 'bottom':
            return p[1] >= y_min
        elif edge == 'top':
            return p[1] <= y_max
    
    def compute_intersection(p1, p2, edge):
        x1, y1 = p1
        x2, y2 = p2
        
        if edge == 'left':
            x = x_min
            y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
        elif edge == 'right':
            x = x_max
            y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
        elif edge == 'bottom':
            y = y_min
            x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
        elif edge == 'top':
            y = y_max
            x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
        
        return [x, y]
    
    def clip_polygon_by_edge(polygon, edge):
        if not polygon:
            return []
        
        clipped = []
        if polygon:
            s = polygon[-1]
            
            for e in polygon:
                if inside(e, edge):
                    if not inside(s, edge):
                        intersection = compute_intersection(s, e, edge)
                        clipped.append(intersection)
                    clipped.append(e)
                elif inside(s, edge):
                    intersection = compute_intersection(s, e, edge)
                    clipped.append(intersection)
                s = e
        
        return clipped
    
    result = polygon[:]
    edges = ['left', 'right', 'bottom', 'top']
    
    for edge in edges:
        result = clip_polygon_by_edge(result, edge)
        if not result:
            break
    
    return result