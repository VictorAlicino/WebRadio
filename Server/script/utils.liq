# Generates an unique UUID
# The UUID looks like a 8-bit hexadecimal UUID like 000000, FFFFFF
# 
# Input: None
# Returns: A string containing an unique UUID
#def generate_new_uuid()
#    pool = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
#    uuid = ref("")
#
#    for i = 0 to 5 do
#        temp = random(pool) # Get a random value from pool list
#        uuid ^ temp # Concatenates the value to string <uuid>
#    end
#
#    if outputs_id.mem(uuid) == true then uuid = generate_new_uuid() # Check if the UUID generated already exists
#
#    uuid # Return the UUID string
#end
