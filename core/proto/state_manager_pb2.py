# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: state_manager.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'state_manager.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13state_manager.proto\x12\x0cstatemanager\"?\n\x1fGetDefinitionFileContentRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"3\n GetDefinitionFileContentResponse\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t\"h\n\x1fSetDefinitionFileContentRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x16\n\x0e\x63ommit_message\x18\x04 \x01(\t\"J\n SetDefinitionFileContentResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\"S\n\x1b\x44\x65leteDefinitionFileRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x16\n\x0e\x63ommit_message\x18\x03 \x01(\t\"F\n\x1c\x44\x65leteDefinitionFileResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\"Q\n\x1eListDefinitionDirectoryRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x11\n\trecursive\x18\x03 \x01(\x08\"z\n\x08\x46ileInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12-\n\x04type\x18\x03 \x01(\x0e\x32\x1f.statemanager.FileInfo.FileType\"#\n\x08\x46ileType\x12\x08\n\x04\x46ILE\x10\x00\x12\r\n\tDIRECTORY\x10\x01\"p\n\x1fListDefinitionDirectoryResponse\x12%\n\x05\x66iles\x18\x01 \x03(\x0b\x32\x16.statemanager.FileInfo\x12\x0f\n\x07success\x18\x02 \x01(\x08\x12\x15\n\rerror_message\x18\x03 \x01(\t\"5\n\x16GetRuntimeValueRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\x12\x0b\n\x03key\x18\x02 \x01(\t\"N\n\x17GetRuntimeValueResponse\x12\r\n\x05\x66ound\x18\x01 \x01(\x08\x12\r\n\x05value\x18\x02 \x01(\t\x12\x15\n\rerror_message\x18\x03 \x01(\t\"D\n\x16SetRuntimeValueRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\"A\n\x17SetRuntimeValueResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\"8\n\x19\x44\x65leteRuntimeValueRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\x12\x0b\n\x03key\x18\x02 \x01(\t\"D\n\x1a\x44\x65leteRuntimeValueResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t2\x94\x06\n\x0cStateManager\x12y\n\x18GetDefinitionFileContent\x12-.statemanager.GetDefinitionFileContentRequest\x1a..statemanager.GetDefinitionFileContentResponse\x12y\n\x18SetDefinitionFileContent\x12-.statemanager.SetDefinitionFileContentRequest\x1a..statemanager.SetDefinitionFileContentResponse\x12m\n\x14\x44\x65leteDefinitionFile\x12).statemanager.DeleteDefinitionFileRequest\x1a*.statemanager.DeleteDefinitionFileResponse\x12v\n\x17ListDefinitionDirectory\x12,.statemanager.ListDefinitionDirectoryRequest\x1a-.statemanager.ListDefinitionDirectoryResponse\x12^\n\x0fGetRuntimeValue\x12$.statemanager.GetRuntimeValueRequest\x1a%.statemanager.GetRuntimeValueResponse\x12^\n\x0fSetRuntimeValue\x12$.statemanager.SetRuntimeValueRequest\x1a%.statemanager.SetRuntimeValueResponse\x12g\n\x12\x44\x65leteRuntimeValue\x12\'.statemanager.DeleteRuntimeValueRequest\x1a(.statemanager.DeleteRuntimeValueResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'state_manager_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_GETDEFINITIONFILECONTENTREQUEST']._serialized_start=37
  _globals['_GETDEFINITIONFILECONTENTREQUEST']._serialized_end=100
  _globals['_GETDEFINITIONFILECONTENTRESPONSE']._serialized_start=102
  _globals['_GETDEFINITIONFILECONTENTRESPONSE']._serialized_end=153
  _globals['_SETDEFINITIONFILECONTENTREQUEST']._serialized_start=155
  _globals['_SETDEFINITIONFILECONTENTREQUEST']._serialized_end=259
  _globals['_SETDEFINITIONFILECONTENTRESPONSE']._serialized_start=261
  _globals['_SETDEFINITIONFILECONTENTRESPONSE']._serialized_end=335
  _globals['_DELETEDEFINITIONFILEREQUEST']._serialized_start=337
  _globals['_DELETEDEFINITIONFILEREQUEST']._serialized_end=420
  _globals['_DELETEDEFINITIONFILERESPONSE']._serialized_start=422
  _globals['_DELETEDEFINITIONFILERESPONSE']._serialized_end=492
  _globals['_LISTDEFINITIONDIRECTORYREQUEST']._serialized_start=494
  _globals['_LISTDEFINITIONDIRECTORYREQUEST']._serialized_end=575
  _globals['_FILEINFO']._serialized_start=577
  _globals['_FILEINFO']._serialized_end=699
  _globals['_FILEINFO_FILETYPE']._serialized_start=664
  _globals['_FILEINFO_FILETYPE']._serialized_end=699
  _globals['_LISTDEFINITIONDIRECTORYRESPONSE']._serialized_start=701
  _globals['_LISTDEFINITIONDIRECTORYRESPONSE']._serialized_end=813
  _globals['_GETRUNTIMEVALUEREQUEST']._serialized_start=815
  _globals['_GETRUNTIMEVALUEREQUEST']._serialized_end=868
  _globals['_GETRUNTIMEVALUERESPONSE']._serialized_start=870
  _globals['_GETRUNTIMEVALUERESPONSE']._serialized_end=948
  _globals['_SETRUNTIMEVALUEREQUEST']._serialized_start=950
  _globals['_SETRUNTIMEVALUEREQUEST']._serialized_end=1018
  _globals['_SETRUNTIMEVALUERESPONSE']._serialized_start=1020
  _globals['_SETRUNTIMEVALUERESPONSE']._serialized_end=1085
  _globals['_DELETERUNTIMEVALUEREQUEST']._serialized_start=1087
  _globals['_DELETERUNTIMEVALUEREQUEST']._serialized_end=1143
  _globals['_DELETERUNTIMEVALUERESPONSE']._serialized_start=1145
  _globals['_DELETERUNTIMEVALUERESPONSE']._serialized_end=1213
  _globals['_STATEMANAGER']._serialized_start=1216
  _globals['_STATEMANAGER']._serialized_end=2004
# @@protoc_insertion_point(module_scope)
