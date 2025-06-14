# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import application_registry_pb2 as application__registry__pb2

GRPC_GENERATED_VERSION = '1.71.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in application_registry_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ApplicationRegistryStub(object):
    """Service for managing application definitions, configuration, and status.
    Interacts with the StateManager for persistent storage.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterApplication = channel.unary_unary(
                '/applicationregistry.ApplicationRegistry/RegisterApplication',
                request_serializer=application__registry__pb2.RegisterApplicationRequest.SerializeToString,
                response_deserializer=application__registry__pb2.RegisterApplicationResponse.FromString,
                _registered_method=True)
        self.UpdateApplication = channel.unary_unary(
                '/applicationregistry.ApplicationRegistry/UpdateApplication',
                request_serializer=application__registry__pb2.UpdateApplicationRequest.SerializeToString,
                response_deserializer=application__registry__pb2.UpdateApplicationResponse.FromString,
                _registered_method=True)
        self.DeregisterApplication = channel.unary_unary(
                '/applicationregistry.ApplicationRegistry/DeregisterApplication',
                request_serializer=application__registry__pb2.DeregisterApplicationRequest.SerializeToString,
                response_deserializer=application__registry__pb2.DeregisterApplicationResponse.FromString,
                _registered_method=True)
        self.GetApplicationStatus = channel.unary_unary(
                '/applicationregistry.ApplicationRegistry/GetApplicationStatus',
                request_serializer=application__registry__pb2.GetApplicationStatusRequest.SerializeToString,
                response_deserializer=application__registry__pb2.GetApplicationStatusResponse.FromString,
                _registered_method=True)
        self.ListActiveApplications = channel.unary_unary(
                '/applicationregistry.ApplicationRegistry/ListActiveApplications',
                request_serializer=application__registry__pb2.ListActiveApplicationsRequest.SerializeToString,
                response_deserializer=application__registry__pb2.ListActiveApplicationsResponse.FromString,
                _registered_method=True)
        self.GetApplicationDetails = channel.unary_unary(
                '/applicationregistry.ApplicationRegistry/GetApplicationDetails',
                request_serializer=application__registry__pb2.GetApplicationDetailsRequest.SerializeToString,
                response_deserializer=application__registry__pb2.GetApplicationDetailsResponse.FromString,
                _registered_method=True)
        self.GetSandboxRequirements = channel.unary_unary(
                '/applicationregistry.ApplicationRegistry/GetSandboxRequirements',
                request_serializer=application__registry__pb2.GetSandboxRequirementsRequest.SerializeToString,
                response_deserializer=application__registry__pb2.GetSandboxRequirementsResponse.FromString,
                _registered_method=True)
        self.GetComponentDefinition = channel.unary_unary(
                '/applicationregistry.ApplicationRegistry/GetComponentDefinition',
                request_serializer=application__registry__pb2.GetComponentDefinitionRequest.SerializeToString,
                response_deserializer=application__registry__pb2.GetComponentDefinitionResponse.FromString,
                _registered_method=True)
        self.GetAppConfigurationValue = channel.unary_unary(
                '/applicationregistry.ApplicationRegistry/GetAppConfigurationValue',
                request_serializer=application__registry__pb2.GetAppConfigurationValueRequest.SerializeToString,
                response_deserializer=application__registry__pb2.GetAppConfigurationValueResponse.FromString,
                _registered_method=True)
        self.ValidateApiKey = channel.unary_unary(
                '/applicationregistry.ApplicationRegistry/ValidateApiKey',
                request_serializer=application__registry__pb2.ValidateApiKeyRequest.SerializeToString,
                response_deserializer=application__registry__pb2.ValidateApiKeyResponse.FromString,
                _registered_method=True)
        self.GetApplicationPermissions = channel.unary_unary(
                '/applicationregistry.ApplicationRegistry/GetApplicationPermissions',
                request_serializer=application__registry__pb2.GetApplicationPermissionsRequest.SerializeToString,
                response_deserializer=application__registry__pb2.GetApplicationPermissionsResponse.FromString,
                _registered_method=True)
        self.GetUserPermissionsForApp = channel.unary_unary(
                '/applicationregistry.ApplicationRegistry/GetUserPermissionsForApp',
                request_serializer=application__registry__pb2.GetUserPermissionsForAppRequest.SerializeToString,
                response_deserializer=application__registry__pb2.GetUserPermissionsForAppResponse.FromString,
                _registered_method=True)


class ApplicationRegistryServicer(object):
    """Service for managing application definitions, configuration, and status.
    Interacts with the StateManager for persistent storage.
    """

    def RegisterApplication(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateApplication(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeregisterApplication(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetApplicationStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListActiveApplications(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetApplicationDetails(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSandboxRequirements(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetComponentDefinition(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAppConfigurationValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ValidateApiKey(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetApplicationPermissions(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserPermissionsForApp(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ApplicationRegistryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterApplication': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterApplication,
                    request_deserializer=application__registry__pb2.RegisterApplicationRequest.FromString,
                    response_serializer=application__registry__pb2.RegisterApplicationResponse.SerializeToString,
            ),
            'UpdateApplication': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateApplication,
                    request_deserializer=application__registry__pb2.UpdateApplicationRequest.FromString,
                    response_serializer=application__registry__pb2.UpdateApplicationResponse.SerializeToString,
            ),
            'DeregisterApplication': grpc.unary_unary_rpc_method_handler(
                    servicer.DeregisterApplication,
                    request_deserializer=application__registry__pb2.DeregisterApplicationRequest.FromString,
                    response_serializer=application__registry__pb2.DeregisterApplicationResponse.SerializeToString,
            ),
            'GetApplicationStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetApplicationStatus,
                    request_deserializer=application__registry__pb2.GetApplicationStatusRequest.FromString,
                    response_serializer=application__registry__pb2.GetApplicationStatusResponse.SerializeToString,
            ),
            'ListActiveApplications': grpc.unary_unary_rpc_method_handler(
                    servicer.ListActiveApplications,
                    request_deserializer=application__registry__pb2.ListActiveApplicationsRequest.FromString,
                    response_serializer=application__registry__pb2.ListActiveApplicationsResponse.SerializeToString,
            ),
            'GetApplicationDetails': grpc.unary_unary_rpc_method_handler(
                    servicer.GetApplicationDetails,
                    request_deserializer=application__registry__pb2.GetApplicationDetailsRequest.FromString,
                    response_serializer=application__registry__pb2.GetApplicationDetailsResponse.SerializeToString,
            ),
            'GetSandboxRequirements': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSandboxRequirements,
                    request_deserializer=application__registry__pb2.GetSandboxRequirementsRequest.FromString,
                    response_serializer=application__registry__pb2.GetSandboxRequirementsResponse.SerializeToString,
            ),
            'GetComponentDefinition': grpc.unary_unary_rpc_method_handler(
                    servicer.GetComponentDefinition,
                    request_deserializer=application__registry__pb2.GetComponentDefinitionRequest.FromString,
                    response_serializer=application__registry__pb2.GetComponentDefinitionResponse.SerializeToString,
            ),
            'GetAppConfigurationValue': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAppConfigurationValue,
                    request_deserializer=application__registry__pb2.GetAppConfigurationValueRequest.FromString,
                    response_serializer=application__registry__pb2.GetAppConfigurationValueResponse.SerializeToString,
            ),
            'ValidateApiKey': grpc.unary_unary_rpc_method_handler(
                    servicer.ValidateApiKey,
                    request_deserializer=application__registry__pb2.ValidateApiKeyRequest.FromString,
                    response_serializer=application__registry__pb2.ValidateApiKeyResponse.SerializeToString,
            ),
            'GetApplicationPermissions': grpc.unary_unary_rpc_method_handler(
                    servicer.GetApplicationPermissions,
                    request_deserializer=application__registry__pb2.GetApplicationPermissionsRequest.FromString,
                    response_serializer=application__registry__pb2.GetApplicationPermissionsResponse.SerializeToString,
            ),
            'GetUserPermissionsForApp': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUserPermissionsForApp,
                    request_deserializer=application__registry__pb2.GetUserPermissionsForAppRequest.FromString,
                    response_serializer=application__registry__pb2.GetUserPermissionsForAppResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'applicationregistry.ApplicationRegistry', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('applicationregistry.ApplicationRegistry', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ApplicationRegistry(object):
    """Service for managing application definitions, configuration, and status.
    Interacts with the StateManager for persistent storage.
    """

    @staticmethod
    def RegisterApplication(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/applicationregistry.ApplicationRegistry/RegisterApplication',
            application__registry__pb2.RegisterApplicationRequest.SerializeToString,
            application__registry__pb2.RegisterApplicationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateApplication(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/applicationregistry.ApplicationRegistry/UpdateApplication',
            application__registry__pb2.UpdateApplicationRequest.SerializeToString,
            application__registry__pb2.UpdateApplicationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeregisterApplication(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/applicationregistry.ApplicationRegistry/DeregisterApplication',
            application__registry__pb2.DeregisterApplicationRequest.SerializeToString,
            application__registry__pb2.DeregisterApplicationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetApplicationStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/applicationregistry.ApplicationRegistry/GetApplicationStatus',
            application__registry__pb2.GetApplicationStatusRequest.SerializeToString,
            application__registry__pb2.GetApplicationStatusResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ListActiveApplications(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/applicationregistry.ApplicationRegistry/ListActiveApplications',
            application__registry__pb2.ListActiveApplicationsRequest.SerializeToString,
            application__registry__pb2.ListActiveApplicationsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetApplicationDetails(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/applicationregistry.ApplicationRegistry/GetApplicationDetails',
            application__registry__pb2.GetApplicationDetailsRequest.SerializeToString,
            application__registry__pb2.GetApplicationDetailsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetSandboxRequirements(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/applicationregistry.ApplicationRegistry/GetSandboxRequirements',
            application__registry__pb2.GetSandboxRequirementsRequest.SerializeToString,
            application__registry__pb2.GetSandboxRequirementsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetComponentDefinition(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/applicationregistry.ApplicationRegistry/GetComponentDefinition',
            application__registry__pb2.GetComponentDefinitionRequest.SerializeToString,
            application__registry__pb2.GetComponentDefinitionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetAppConfigurationValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/applicationregistry.ApplicationRegistry/GetAppConfigurationValue',
            application__registry__pb2.GetAppConfigurationValueRequest.SerializeToString,
            application__registry__pb2.GetAppConfigurationValueResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ValidateApiKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/applicationregistry.ApplicationRegistry/ValidateApiKey',
            application__registry__pb2.ValidateApiKeyRequest.SerializeToString,
            application__registry__pb2.ValidateApiKeyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetApplicationPermissions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/applicationregistry.ApplicationRegistry/GetApplicationPermissions',
            application__registry__pb2.GetApplicationPermissionsRequest.SerializeToString,
            application__registry__pb2.GetApplicationPermissionsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetUserPermissionsForApp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/applicationregistry.ApplicationRegistry/GetUserPermissionsForApp',
            application__registry__pb2.GetUserPermissionsForAppRequest.SerializeToString,
            application__registry__pb2.GetUserPermissionsForAppResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
