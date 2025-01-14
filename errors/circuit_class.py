"""
Error Codes for the Methods in the CircuitClass Service
"""

# List
circuit_circuit_class_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
circuit_circuit_class_create_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
circuit_circuit_class_create_102 = 'The "name" parameter is invalid. "name" cannot be longer than 250 characters.'
circuit_circuit_class_create_103 = (
    'The "name" parameter is invalid. A CircuitClass with that name already exists for your Member.'
)
circuit_circuit_class_create_104 = 'The "properties" parameter is invalid. "properties" must be an array.'
circuit_circuit_class_create_105 = 'The "properties" parameter is invalid. "properties" array  cannot be empty.'
circuit_circuit_class_create_106 = 'The "properties" parameter is invalid. Each item in the array must be an object.'
circuit_circuit_class_create_107 = (
    'The "properties" parameter is invalid. "property_type_id" is required for each item in the array "properties".'
)
circuit_circuit_class_create_108 = (
    'The "properties" parameter is invalid. One of the sent values for "property_type_id" does not belong to a valid '
    'PropertyType record.'
)
circuit_circuit_class_create_109 = (
    'The "properties" parameter is invalid. "key" is required for each item in the array "properties"'
)
circuit_circuit_class_create_110 = (
    'The "properties" parameter is invalid. "key" cannot be longer than 250 characters for each item in the array '
    '"properties".'
)
circuit_circuit_class_create_111 = (
    'The "properties" parameter is invalid. "key" must be unique within the array of "properties".'
)
circuit_circuit_class_create_112 = (
    'The "properties" parameter is invalid. "required" is required for each item in the array "properties"'
)
circuit_circuit_class_create_113 = (
    'The "properties" parameter is invalid. "required" must be a boolean for each item in the array "properties".'
)
circuit_circuit_class_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'

# Read
circuit_circuit_class_read_001 = (
    'The "pk" parameter is invalid. "pk" does not belong to any valid CircuitClass in your Member.'
)

# Update
circuit_circuit_class_update_001 = (
    'The "pk" path parameter is invalid. "pk" must belong to a valid  CircuitClass record.'
)
circuit_circuit_class_update_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
circuit_circuit_class_update_102 = 'The "name" parameter is invalid. "name" cannot be longer than 250 characters.'
circuit_circuit_class_update_103 = (
    'The "name" parameter is invalid. A CircuitClass with that name already exists for your Member.'
)
circuit_circuit_class_update_104 = 'The "properties" parameter is invalid. "properties" must be an array.'
circuit_circuit_class_update_105 = 'The "properties" parameter is invalid. "properties" cannot be empty.'
circuit_circuit_class_update_106 = (
    'The "properties" parameter is invalid. This Circuit Class has associated Circuits with the current properties. All'
    'keys for the current properties must be included as items in the array '
)
circuit_circuit_class_update_107 = 'The "properties" parameter is invalid. Each item in the array must be an object.'
circuit_circuit_class_update_108 = (
    'The "properties" parameter is invalid. "property_type_id" is required for each item in the array "properties".'
)
circuit_circuit_class_update_109 = (
    'The "properties" parameter is invalid. One of the sent values for "property_type_id" does not belong to a valid '
    'PropertyType record.'
)
circuit_circuit_class_update_110 = (
    'The "properties" parameter is invalid. "key" is required for each item in the array "properties"'
)
circuit_circuit_class_update_111 = (
    'The "properties" parameter is invalid. "key" cannot be longer than 250 characters for each item in the array '
    '"properties".'
)
circuit_circuit_class_update_112 = (
    'The "properties" parameter is invalid. "key" must be unique within the array of "properties".'
)
circuit_circuit_class_update_113 = (
    'The "properties" parameter is invalid. "required" is required for each item in the array "properties"'
)
circuit_circuit_class_update_114 = (
    'The "properties" parameter is invalid. "required" must be a boolean for each item in the array "properties".'
)
# Delete
circuit_circuit_class_delete_001 = (
    'The "pk" path parameter is invalid. "pk" must belong to a valid CircuitClass record.'
)
circuit_circuit_class_delete_201 = (
    'You do not have permission to make this request. You cannot delete a Circuit Class that is associated with '
    'one or more Circuits.'
)
