

def access_common_data(request,*args,**kwargs):
    """
      The context processor must return a dictionary.
    """
    return {'id_user':request.user.id ,"kwargs":kwargs,'args':args } 