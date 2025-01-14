"""
Error Codes for all the Methods in the Circuit Service
"""

# List
circuit_circuit_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
circuit_circuit_create_101 = 'The "bandwidth" parameter is invalid. "bandwidth" must be an integer.'
circuit_circuit_create_102 = (
    'The "circuit_class_id" parameter is invalid. "circuit_class_id" is required and must be an integer.'
)
circuit_circuit_create_103 = 'The "circuit_class_id" parameter is invalid. "circuit_class_id" must be an integer.'
circuit_circuit_create_104 = (
    'The "circuit_class_id" parameter is invalid. "circuit_class_id" does not belong to a valid Circuit record'
)
circuit_circuit_create_106 = (
    'The "customer_address_id" parameter is invalid. "customer_address_id" must be an integer.'
)
circuit_circuit_create_107 = (
    'The "customer_address_id" parameter is invalid. You must be linked to an Address to create aCircuit for them as '
    'the customer.'
)
circuit_circuit_create_108 = (
    'The "hand_off_point" parameter is invalid. "hand_off_point" cannot be longer than 20 characters.'
)
circuit_circuit_create_109 = 'The "install_date" parameter is invalid. "install_date" is required.'
circuit_circuit_create_110 = (
    'The "install_date" parameter is invalid. "install_date" must be a date string in isoformat.'
)
circuit_circuit_create_111 = (
    'The "decommission_date" parameter is invalid. "decommission_date" must be a date string in isoformat.'
)

circuit_circuit_create_112 = (
    'The "decommission_date" parameter is invalid. "decommission_date" cannot be before the specified "install_date".'
)
circuit_circuit_create_113 = 'The "properties" parameter is invalid. "properties" should be a dict'
circuit_circuit_create_114 = (
    'The "properties" parameter is invalid. A required key for the Circuit Class Property Type was not sent as a key.'
)
circuit_circuit_create_115 = (
    'The "properties" parameter is invalid. On of the sent values(numeric) in the dictionary must be an integer, '
    'float, complex or Decimal.'
)
circuit_circuit_create_116 = (
    'The "properties" parameter is invalid. On of the sent values(link) in the dictionary must be a URL.'
)
circuit_circuit_create_117 = (
    'The "properties" parameter is invalid. On of the sent values(network) in the dictionary must be a valid IPv6 or '
    'IPv4 address or network.'
)
circuit_circuit_create_118 = (
    'The "properties" parameter is invalid. A required key for the Circuit Class Property Type was sent as a key with '
    'no value.'
)
circuit_circuit_create_119 = 'The "reference" parameter is invalid. "reference" cannot be longer than 100 characters.'
circuit_circuit_create_121 = (
    'The "service_provider_address_id" parameter is invalid. "service_provider_address_id" must be an integer.'
)
circuit_circuit_create_122 = (
    'The "service_provider_address_id" parameter is invalid. You must be linked to an Address to create a'
    'Circuit for them as the service provider.'
)
circuit_circuit_create_123 = (
    'The "group_name" parameter is invalid. "group_name" cannot be longer than 250 characters.'
)
circuit_circuit_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'

# READ
circuit_circuit_read_001 = 'The "pk" parameter is invalid. "pk" must belong to a valid Circuit record.'
circuit_circuit_read_201 = (
    'You do not have permission to execute this method. You can only read a Circuit where either "address_id", '
    '"service_provider_address_id" or "customer_address_id" is an Address in your Member.'
)
circuit_circuit_read_202 = (
    'You do not have permission to make this request. You can only read a Circuit where either "address_id", '
    '"service_provider_address_id" or "customer_address_id" is your Address.'
)


# Update
circuit_circuit_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Circuit record.'
circuit_circuit_update_101 = 'The "bandwidth" parameter is invalid. "bandwidth" must be an integer.'

circuit_circuit_update_103 = 'The "customer_address_id" parameter is invalid. "customer_address_id" must be an integer.'
circuit_circuit_update_104 = (
    'The "customer_address_id" parameter is invalid. You must be linked to an Address to update a Circuit for them as '
    'the customer.'
)
circuit_circuit_update_105 = (
    'The "hand_off_point" parameter is invalid. "hand_off_point" cannot be longer than 20 characters.'
)
circuit_circuit_update_106 = (
    'The "install_date" parameter is invalid. "install_date" is required.'
)
circuit_circuit_update_107 = (
    'The "install_date" parameter is invalid. "install_date" must be a date string in isoformat.'
)
circuit_circuit_update_108 = (
    'The "decommission_date" parameter is invalid. "decommission_date" must be a date string in isoformat.'
)

circuit_circuit_update_109 = (
    'The "decommission_date" parameter is invalid. "decommission_date" cannot be before the specified "install_date".'
)
circuit_circuit_update_110 = (
    'The "properties" parameter is invalid. "properties" should be a dict'
)
circuit_circuit_update_111 = (
    'The "properties" parameter is invalid. A required key for the Circuit Class Property Type was not sent as a key.'
)
circuit_circuit_update_112 = (
    'The "properties" parameter is invalid. On of the sent values(numeric) in the dictionary must be an integer, '
    'float, complex or Decimal.'
)
circuit_circuit_update_113 = (
    'The "properties" parameter is invalid. On of the sent values(link) in the dictionary must be a URL.'
)
circuit_circuit_update_114 = (
    'The "properties" parameter is invalid. On of the sent values(network) in the dictionary must be a valid IPv6 or '
    'IPv4 address or network.'
)
circuit_circuit_update_115 = (
    'The "properties" parameter is invalid. A required key for the Circuit Class Property Type was sent as a key with '
    'no value.'
)
circuit_circuit_update_116 = 'The "reference" parameter is invalid. "reference" cannot be longer than 100 characters.'
circuit_circuit_update_118 = (
    'The "service_provider_address_id" parameter is invalid. "service_provider_address_id" must be an integer.'
)
circuit_circuit_update_119 = (
    'The "service_provider_address_id" parameter is invalid. You must be linked to an Address to update a'
    'Circuit for them as the service provider.'
)
circuit_circuit_update_120 = (
    'The "group_name" parameter is invalid. "group_name" cannot be longer than 250 characters.'
)
# Delete
circuit_circuit_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Circuit record.'
