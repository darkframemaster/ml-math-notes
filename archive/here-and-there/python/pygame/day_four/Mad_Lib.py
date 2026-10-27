#!/usr/bin/env python2.7

print("MAD LIB GAME")
print("Enter answers to the following prompts")

guy=raw_input("Name of a famous man:")
girl=raw_input("Name of a famous woman:")
food=raw_input("Your favorite food (plural):")
ship=raw_input("Name of a space ship:")
job=raw_input("Name if a profession (plural):")
planet=raw_input("Name of a planet:")
drink=raw_input("Your favorite drink:")
number=raw_input("A number from 1 to 10:")

story="\nA famous married couple,GUY and GIRL,went on\n"+"vacation to the planet PLANET.It took NUMBER\n"+"weeks to get there travelling by SHIP.They\n"+"enjoy a luxurious candlelight dinner over-\n"+"looking a DRINK ocean while eating FOOD.But,\n"+"since they were both JOB,they had to cut their\n"+"vacation short."

story=story.replace("GUY",guy)
story=story.replace("GIRL",girl)
story=story.replace("FOOD",food)
story=story.replace("SHIP",ship)
story=story.replace("JOB",job)
story=story.replace("PLANET",planet)
story=story.replace("DRINK",drink)
story=story.replace("NUMBER",number)
print(story)

