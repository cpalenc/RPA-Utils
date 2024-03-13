def extract_first_match(args):      
    try:
        import re
        import traceback
        args_splitted = args.split("||")
        print((args_splitted))
        regex_pattern = args_splitted[0]
        text = args_splitted[1]
        regex = re.compile(regex_pattern)
        print(f"{regex = }")
        match = regex.search(text)
        if match:
            return match.group()
        return "No se encontraron coincidencias."
    except Exception:
        return traceback.format_exc()



import os
import re
import extract_msg
import json
import sys
import traceback
import datetime

        
def validate_path(path):
    if os.path.exists(path):
        return True
    else:
        return False
    
def log_message(message, file_path, error=False):
    if error:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = {
            'filename': exc_traceback.tb_frame.f_code.co_filename,
            'line': exc_traceback.tb_lineno,
            'name': exc_traceback.tb_frame.f_code.co_name,
        }    
    with open(file_path, 'a') as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        register = f"filename:{traceback_details['filename']} line:{traceback_details['line']} func:{traceback_details['name']} {message}" if error else message 
        log_file.write(f"{timestamp}{register}\n")
        
def split_argsuments_automation(args):
    return args.split("||")

def extract_pdfs_from_msg(msg_file, destination, log_path):
    file_name_without_extension = ""
    attachments_pdf = []
    try:
        msg = extract_msg.Message(msg_file)
        file_name_without_extension = os.path.splitext(os.path.basename(msg_file))[0]
        today = datetime.datetime.now().strftime('%Y_%m_%d')
        msg_folder = os.path.join(f"{destination}/{today}", file_name_without_extension)    
        if not os.path.exists(msg_folder): 
            os.makedirs(msg_folder)            
        metadata = {
            'subject': msg.subject,
            'sender': msg.sender,
            'date': str(msg.date)
        }
        path_metadata_file = os.path.join(msg_folder, 'metadata.json')
        with open(path_metadata_file, 'w') as metadata_file:
            json.dump(metadata, metadata_file)
        for attachment in msg.attachments:
            file_name = attachment.longFilename or attachment.shortFilename
            if file_name and file_name.lower().endswith('.pdf'):
                pdf_path = os.path.join(msg_folder, file_name)
                attachments_pdf.append(file_name)
                with open(pdf_path, 'wb') as pdf_file:
                    pdf_file.write(attachment.data)                
        msg.close()

        log_message(f"success extraction file: {file_name_without_extension}", log_path)
        return (True, attachments_pdf, msg_folder)
    
    except Exception as e:        
        log_message( f"{file_name_without_extension} {e = }", log_path, error=True)
        return (False,f"error extracting file: {file_name_without_extension}")


def process_msgs_in_folder(args):
    try:
        queries = []
        args = split_argsuments_automation(args)
        args_enough = len(args)
        if args_enough < 4:
            return f"Error - Incomplete parameters: expected 4 but {args_enough} were given"
        
        folder_path = args[0]    
        destination = args[1]
        log_path = args[2]
        processed_files = eval(args[3])
        
        if not os.path.exists(folder_path):
            return f"Error - Path '{folder_path}' doesn't exist"
        
        total_files = 0
        files_extracted = 0
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.msg') and file not in (processed_files):
                    msg_file = os.path.join(root, file)
                    response = extract_pdfs_from_msg(msg_file, destination, log_path)                    
                    files_extracted += 1 if response[0] else files_extracted
                    total_files += 1
                    queries.append(build_query(file, ''.join(response[1]), response[2]))
                                                    
        if total_files == 0:
            return "there are not files"
        return '||'.join(queries)
    
    except Exception as e:
        log_message( f"{response = } {e = }", log_path, error=True)        
        return(f"Error: {e}")   
    

def build_query(msg_name, extracted_files, folder_path ):
    return f"INSERT INTO R178_Extracted_msg (msg_name, extracted_files, folder_path, estado) VALUES ('{msg_name}', '{extracted_files}', '{folder_path}', 'Extracted')"

def test(folder_path):
   # return f"{type(folder_path)} {folder_path = }"
    return process_msgs_in_folder(folder_path)
    
def validate_type(some):
    return str(type(some))
   


def rename_files(folder_path):
    import os
    import traceback
    try:
        files = os.listdir(folder_path)
        for file_name in files:
            if os.path.isfile(os.path.join(folder_path, file_name)):
                base_name, extension = os.path.splitext(file_name)
                if not base_name.endswith("_proc_bbot"):
                    new_name = f"{base_name}_proc_bbot{extension}"
                    os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_name))
                    print(f"Renamed: {file_name} -> {new_name}")
        return "Success"
    except Exception:
        return "Error:\n" + traceback.format_exc()


    