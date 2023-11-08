import os
from selenium import webdriver;
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def calculateLateSubmitScore(maxScore, lateHours):
    print("The return of this assignment is " + str(lateHours) + " hours late")
    return maxScore * (1 - (0.5 / 336) * lateHours)

def getUrl():
    if(not os.path.exists("url.txt")):
        return saveUrl()
    else:
        with open("url.txt", 'r') as txtFile:
            url = txtFile.readline()
            return url

def saveUrl():
        #When using for the first time you need to provide url to Moodle
        #And it will be saved in the root of this project in .txt file
        askUrl = input("Give the url to Moodle: ")
        with open("url.txt", 'w') as txtFile:
                txtFile.write(askUrl)
        return askUrl

def main():
    driver = webdriver.Chrome()
    driver.get(getUrl())

    while(True):
        check = input("Navigate to the grade view and press enter: ")
        if(check == "exit"):
            break

        delay = input("Enter the delay time between page changes (default delay is 4 sec): ")
        if not delay: 
            delay = 4
        delay = int(delay)

        maxScore = int(input("Enter the maximum score for the assignment: "))

        #uncheck notify student checkbox
        checkbox = driver.find_element(By.XPATH, '//*[@id="page"]/section/div[2]/div[4]/div/div[2]/form/label/input')
        if(checkbox.is_enabled()):
            checkbox.click()

        while(True):
            #Wait until the page is fully loaded
            driver.implicitly_wait(delay)

            #Default score is the maximum if the return is not late
            score = maxScore

            #If the student has returned the assignment in text format
            #Need to expand the text field
            try:
                wait = WebDriverWait(driver, 2)
                element_locator = (By.CSS_SELECTOR, 'i.icon.fa.fa-plus.fa-fw[title="View full"][role="img"][aria-label="View full"]')
                plusIcon = wait.until(EC.visibility_of_element_located(element_locator))
                plusIcon.click()
            except:
                pass

            try:
                #If the student has returned the assignment late
                lateSubmissionString = driver.find_element(By.CLASS_NAME, 'latesubmission')
                strLateSubmissionString = lateSubmissionString.text
                values = [int(s) for s in strLateSubmissionString.split() if s.isdigit()]
                
                if("day" in strLateSubmissionString):
                    days = values[0]
                    hours = values[1]
                    totalHours = (days * 24) + hours
                    score = round(calculateLateSubmitScore(maxScore, totalHours), 2)
                elif("hour" in strLateSubmissionString):
                    hours = values[0]
                    score = round(calculateLateSubmitScore(maxScore, hours), 2)
            except:
                pass
        
            userInput = input("Score (default calculated score is: " + str(score) + "): ")

            if not userInput: 
                userInput = score
            elif(userInput == "exit"):
                break

            element = driver.find_element(By.ID, 'id_grade')
            element.submit()
            element.send_keys(userInput)

            #Wait one second before click (for seeing the score in the input)
            driver.implicitly_wait(1)
            
            element = driver.find_element(By.NAME, 'saveandshownext')
            element.click()

main()