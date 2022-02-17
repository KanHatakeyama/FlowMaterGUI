noise_list=[
"DoesNotExist",
"MultipleObjectsReturned",
"check",
"clean",
"clean_fields",
"date_error_message",
"delete",
"from_db",
"full_clean",
"get_deferred_fields",
#"id",
#"level",
#"level_id",
#"pk",
"prepare_database_save",
"refresh_from_db",
"save",
"save_base",
"serializable_value",
#"title_id",
"unique_error_message",
"validate_unique",
]


def collect_attributes(row,obj,title=""):
    if title!="":
        title=f"{title}_"
 
    for i in dir(obj):
        try:
            if str(i)[0]!="_" and i not in noise_list:
                row[f"{title}{i}"]=getattr(obj,i)
        except:
            pass

    return