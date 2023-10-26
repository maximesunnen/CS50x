# Backend helper function to check if a form is filled in by checking the dictionary content

def form_filled_in(dict):
    for key, value in dict.items():
        if not value:
            return False
    return True
    