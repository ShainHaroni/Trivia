# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT",
"get_score": "MYSCORE",
"get_high_score": "HIGHSCORE",
"get_question": "GET_QUESTION",
"get_users" : "GET_USERS",
"get_answer" : "GET_ANSWER",
"get_update_score" : "GET_UPDATE_SCORE"
} # .. Add more commands if needed



PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"logout_msg" : "LOGOUT",
"login_failed_msg" : "ERROR",
"get_score_msg" : "YOUR_SCORE",
"get_high_score_msg" : "ALL_SCORE",
"get_question_msg" : "SEND_QUESTION",
"get_users_msg" : "GET_ALL_USERS",
"get_answer_msg" : "GET_ALL_ANSWER",
"get_update_score_msg" : "GET_UPDATE_SCORE"

} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
    """

    lengthOfData = len(data)
    mid = "|000"
    end = "|"

    full_msg = cmd + "           " + mid + str(lengthOfData) + end + data

    return full_msg




def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """

    str_list = data.split("|", 2)
    if len(str_list) != 3:
        return None, None
    length = len(str_list[2])
    str_list[0] = str_list[0].strip()
    str_list[1] = str_list[1].strip()
    if not str_list[1].isdigit():
        return None, None
    elif int(str_list[1]) != length:
        return None, None
    else:
        return tuple(str_list[::2])



def split_data(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    delimiter = DATA_DELIMITER
    if len(msg) > 22:
        if msg[16] == "|" and msg[21] == "|":
            delimiter = DELIMITER

    msg_split = msg.split(delimiter)
    if len(msg_split) == expected_fields:
        return msg_split
    elif len(msg_split) > expected_fields:
        new = msg.partition("#")
        msg_split = new[0], new[-1]
        return msg_split
    else:
        print('ERROR THE expected_fields > msg')
        return None




def join_data(msg_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    msg_fields = [str(i) for i in msg_fields]
    return DATA_DELIMITER.join(msg_fields)

