from selenium import webdriver;
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def calculateLateSubmitScore(maxScore, lateHours):
    print("The return of this assignment is " + str(lateHours) + " hours late")
    return maxScore * (1 - (0.5 / 336) * lateHours)

def main():
    driver = webdriver.Chrome()
    driver.get("https://elearn.uef.fi/")

    input("Login, navigate to review view and press enter: ")
    maxScore = int(input("Enter the maximum score for the assignment: "))

    #uncheck notify student checkbox
    checkbox = driver.find_element(By.XPATH, '//*[@id="page"]/section/div[2]/div[4]/div/div[2]/form/label/input')
    if(checkbox.is_enabled()):
        checkbox.click()

    while(True):
        #Wait until the page is fully loaded
        driver.implicitly_wait(1)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.submissionstatustable')))
        driver.implicitly_wait(3)

        #Default score is the maximum if the return is not late
        score = maxScore

        #If the student has returned the assignment in text format
        #Need to expand the text field
        try:
            plusIcon = driver.find_element(By.CSS_SELECTOR, 'i.icon.fa.fa-plus.fa-fw::before')
            plusIcon.click()
        except:
            pass

        try:
            #If the student has returned the assignment late
            lateSubmissionString = driver.find_element(By.CLASS_NAME, 'latesubmission')
            strLateSubmissionString = lateSubmissionString.text
            values = [int(s) for s in strLateSubmissionString.split() if s.isdigit()]
            print(values)
            if("day" in strLateSubmissionString):
                days = values[0]
                hours = values[1]
                totalHours = (days * 24) + hours
                score = round(calculateLateSubmitScore(maxScore, totalHours), 2)
            elif("hour" in strLateSubmissionString):
                hours = values[0]
                score = round(calculateLateSubmitScore(maxScore, hours), 2)
            else:
                #Late for less than an hour
                score = round(calculateLateSubmitScore(maxScore, 1), 2)
        except:
            pass
    
        userInput = input("Score (default calculated score is: " + str(score) + "): ")
        if not userInput: 
            userInput = score
        element = driver.find_element(By.ID, 'id_grade')
        element.click()
        element.send_keys(userInput)

        #Wait one second before click (for seeing the score in the input)
        driver.implicitly_wait(1)
        
        element = driver.find_element(By.NAME, 'saveandshownext')
        element.click()

main()