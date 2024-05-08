from pydantic import BaseModel, Field, constr, validator, ConfigDict, ValidationError
from typing import Optional
from typing import List
from typing import Dict
from typing import Union, Annotated
from typing_extensions import TypedDict
from enum import Enum
from enigmapython import *
from enigmapython.SwappablePlugboard import SwappablePlugboard
from enigmapython.Rotor import Rotor 
from enigmapython.Reflector import Reflector
from enigmapython.EtwPassthrough import EtwPassthrough
from enigmapython.Enigma import Enigma


allowed_chars_regex = r"^[A-Z]+$"


class RequestRotorConfig (BaseModel):
    position: int = Field(ge=0, le=25, default=0)
    ring: int = Field(ge=0, le=25, default=0)

class ResponseRotorConfig (BaseModel):
    position: int = Field(ge=0, le=25, default=0)

class PlugboardWiring(BaseModel):
    from_letter: str = Field(regex=allowed_chars_regex, min_length=1, max_length=1)
    to_letter: str = Field(regex=allowed_chars_regex, min_length=1, max_length=1)

class Plugboard (BaseModel):
    wirings: List[PlugboardWiring] = Field(max_items=10)

class EnigmaBaseRequest (BaseModel):
    plugboard: Optional[Plugboard]
    auto_increment_rotors: bool = Field(default=True)
    cleartext: str = Field(regex=allowed_chars_regex, min_length=1, max_length=128)

class EnigmaBaseResponse (BaseModel):
    cyphertext: str
    rotors: List[ResponseRotorConfig]

class EnigmaIRotorsEnum(str, Enum):
    rotor_I = 'I'
    rotor_II = 'II'
    rotor_III = 'III'

class EnigmaIReflectorsEnum(str, Enum):
    reflector_A = 'UKW-A'
    reflector_B = 'UKW-B'
    reflector_C = 'UKW-C'

class EnigmaIRequestRotorConfig (RequestRotorConfig):
    type: EnigmaIRotorsEnum

class EnigmaIRequest(EnigmaBaseRequest):
    rotors: List[EnigmaIRequestRotorConfig] = Field(min_items=3, max_items=3)
    reflector: Optional[EnigmaIReflectorsEnum]
     
class EnigmaIResponse(EnigmaBaseResponse):
    pass

def main(args):
    path_string = args.get("__ow_path")[1:]
    path_elements = path_string.split("/")
    if len(path_elements) == 2:
        match path_elements[0]:
            case "I":
                try:
                    request = EnigmaIRequest(
                                auto_increment_rotors=args.get("auto_increment_rotors"),
                                cleartext=args.get("cleartext"),
                                rotors=args.get("rotors"),
                                reflector=args.get("reflector"),
                                plugboard=args.get("plugboard")
                                )
                except ValidationError as e:
                    return {
                        "statusCode": 400,
                        "body": e.errors()
                        }
                match path_elements[1]:
                    case "encrypt":

                        rotors = []
                        for i in range(len(request.rotors)):
                            rotor = Rotor.get_instance_from_tag("I_"+request.rotors[i].type)
                            rotor.position = request.rotors[i].position
                            rotor.ring = request.rotors[i].ring
                            rotors.append(rotor)
                        #rotors.reverse()
                        
                        reflector = Reflector.get_instance_from_tag(request.reflector)

                        etw = EtwPassthrough()

                        plugboard = SwappablePlugboard()   
                        for plugboard_wiring in request.plugboard.wirings:
                            plugboard.swap(plugboard_wiring.from_letter.lower(),plugboard_wiring.to_letter.lower())

                        enigma = Enigma(
                            plugboard = plugboard,
                            rotors = rotors,
                            reflector = reflector,
                            etw = etw,
                            auto_increment_rotors = request.auto_increment_rotors
                            )
                        

                        cypher_text = enigma.input_string(request.cleartext.lower()).upper()
    
                        new_rotors : ResponseRotorConfig = []
                        for i in range(len(enigma.rotors)):
                            response_rotor_config = ResponseRotorConfig(position=enigma.rotors[i].position,ring=enigma.rotors[i].ring)
                            new_rotors.append(response_rotor_config)
                        #new_rotors.reverse()

                        response = EnigmaIResponse(cyphertext=cypher_text,rotors=new_rotors)
                        
                        return {"body": response.model_dump()}
                    
                    case _:
                        return {
                            "statusCode": 404,
                            "body": {"error":"Resource not found"}
                        }
            case _:
                return {
                    "statusCode": 404,
                    "body": {"error":"Resource not found"}
                }
    else:
        return {
                "statusCode": 404,
                "body": {"error":"Resource not found"}
               }