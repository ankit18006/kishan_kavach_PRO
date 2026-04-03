
def calculate_ai(t,h,g,c):
    if t>30 or h>80 or g>400:
        return {"risk":"HIGH","health_score":40,"days_remaining":2}
    elif t>25:
        return {"risk":"MEDIUM","health_score":70,"days_remaining":5}
    else:
        return {"risk":"LOW","health_score":90,"days_remaining":10}
