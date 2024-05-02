from pydantic import BaseModel, Field, constr, validator, ConfigDict
from typing import Optional
from typing import List
from typing import Dict
from typing import Union, Annotated
from typing_extensions import TypedDict
from enum import Enum
import os


allowed_chars_regex = r"^[A-Z]+$"


class RotorConfig (BaseModel):
    position: int = Field(ge=0, le=25, default=0)
    ring: int = Field(ge=0, le=25, default=1)

class Rotors (BaseModel):
    List[RotorConfig] 

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

class EnigmaIRotorsEnum(str, Enum):
    rotor_I = 'I'
    rotor_II = 'II'
    rotor_III = 'III'

class EnigmaIReflectorsEnum(str, Enum):
    reflector_A = 'UKW-A'
    reflector_B = 'UKW-B'
    reflector_C = 'UKW-C'

class EnigmaIRotorConfig (RotorConfig):
    type: EnigmaIRotorsEnum

class EnigmaIRequest(EnigmaBaseRequest):
    rotors: List[EnigmaIRotorConfig] = Field(min_items=3, max_items=3)
    reflector: Optional[EnigmaIReflectorsEnum]
     
class EnigmaIResponse(EnigmaBaseResponse):
    pass

def main(args):
  print(args)
  print(os.environ.get('__OW_PATH'))
  print(os.environ.get('__OW_API_HOST'))
  return args