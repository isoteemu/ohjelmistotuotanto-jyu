*** Settings ***
Resource  resource.robot

*** Test Cases ***
Register With Valid Username And Password
    Create User  kalle  kalle123
    Input Login Command
    Input Credentials  kalle  kalle123
    Output Should Contain  Logged in


Register With Already Taken Username And Valid Password
    Create User  kalle  kalle123
    Run Keyword And Expect Error  *User with username kalle already exists*  Create User  kalle  kalle123


Register With Too Short Username And Valid Password
    Run Keyword And Expect Error  *Username must be at least 3 characters long*  Create User  ka  kalle123

Register With Enough Long But Invalid Username And Valid Password
    Run Keyword And Expect Error  *UserInputError: Username must only contain characters a-z*  Create User  kalle123  kalle123

Register With Valid Username And Too Short Password
    Run Keyword And Expect Error  *Password must be at least 8 characters long*  Create User  kalle  kalle

Register With Valid Username And Long Enough Password Containing Only Letters
    Run Keyword And Expect Error  *Password must contain at least one non-alphabetic character*  Create User  kalle  kallekalle
