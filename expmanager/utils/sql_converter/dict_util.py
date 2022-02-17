

def change_dict_key(d, old_key, new_key, default_value=None):
    d[new_key] = d.pop(old_key, default_value)


def nested_to_plain_dict(obj):

    rename_keys = [
        ("name", "label"),
        ("mutual_key_title", "ID"),
    ]

    avoid_keys = [
        "special_memo"
    ]
    plain_dict = {}

    def inner_loop(obj, header=""):
        if type(obj) is dict:
            for k, v in obj.items():
                inner_loop(v, f"{header}_{k}")

        elif type(obj) is list:
            for num, sun_obj in enumerate(obj):
                #inner_loop(sun_obj, f"{header}_{num}")
                inner_loop(sun_obj, f"{header}_")

        elif type(obj) is str or type(obj) is bool or type(obj) is int or type(obj) is float:

            for i in range(1000):
                if i==0:
                    key_name=header[1:]
                else:
                    key_name=header[1:]+"_"+str(i+1)

                if key_name not in plain_dict:
                    plain_dict[key_name]=obj
                    break
        
            #plain_dict[header[1:]] = obj

    inner_loop(obj)

    for i in rename_keys:
        change_dict_key(plain_dict, i[0], i[1])

    for i in avoid_keys:
        for key in list(plain_dict):
            if key.find(i) >= 0:
                plain_dict.pop(key)

    return plain_dict
