import names, random

vowels = set('aeiouAEIOU')
vowels_list = ["a", "e", "i", "o", "u"]

def system_name():
    # generate a first name, at least 5 characters long
    first_name = names.get_first_name()
    while (len(first_name) < 5):
        first_name = names.get_first_name()
    #print(first_name)
    first_half = len(first_name) // 2
    # take random amount from first few letters
    prefix = first_name[:random.randint(2, first_half)]
    #print(prefix)


    # generate a last name, at least 5 characters long
    last_name = names.get_last_name()
    while (len(last_name) < 5):
        last_name = names.get_last_name()
    #print(last_name)
    last_half = len(last_name) // 2
    # take a random amount from last few letters
    suffix = last_name[random.randint(2, last_half):]
    #print(suffix)


    # combine the two 
    system_name = prefix + suffix
    #print(system_name)

    # add a vowel at the end if there is none
    if vowels.isdisjoint(system_name):
        system_name = system_name + random.choice(vowels_list)


    #print(system_name)

    # return the system name
    return system_name

if __name__ == '__main__':
    system_name()


# for reference:
'''
>>> x = "Hello World!"
>>> x[2:]
'llo World!'
>>> x[:2]
'He'
>>> x[:-2]
'Hello Worl'
>>> x[-2:]
'd!'
>>> x[2:-2]
'llo Worl'
'''