# Course-owned exercise programs. These never depend on your code.
#
# They are deliberately small, self-contained, and (some of them) deliberately
# broken. You run them, watch them misbehave, and then find out why.

# Stage 6: returns a reference to a dead local. Prints plausible garbage,
# then gets caught red-handed by AddressSanitizer.
add_executable(exercise_dangling dangling.cpp)

add_executable(exercise_dangling_asan dangling.cpp)
target_compile_options(exercise_dangling_asan PRIVATE -fsanitize=address,undefined -g)
target_link_options(exercise_dangling_asan    PRIVATE -fsanitize=address,undefined)

# Stage 4: reads past the end of an array. Used for the first gdb session.
add_executable(exercise_outofbounds outofbounds.cpp)
target_compile_options(exercise_outofbounds PRIVATE -g)
