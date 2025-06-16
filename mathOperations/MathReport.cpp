#include "MathReport.h"
#include <iomanip>
#include <list>

using namespace std;

// default constructor
MathReport::MathReport()
{
}

// add a newQuestion into the vector of mathQuestions
// and the response to check with the correct answer:
//    if response is correct, increase numCorrectAnswers
//    otherwise, increase numWrongAnswers and also insert newQuestion to errorList
void MathReport::insert(MathOperations newQuestion, int response)
{
    mathQuestions.push_back(newQuestion);
    if(newQuestion.checkAnswer(response)){
        numCorrectAnswers++;
    }
    else{
        errorList.push_back(newQuestion);
        numWrongAnswers++;
    }

}

// return the value of numCorrectAnswers
int MathReport::getNumOfCorrectAnswers() const
{
    return numCorrectAnswers;
}

// return the value of numWrongAnswers
int MathReport::getNumOfWrongAnswers() const
{
    return numWrongAnswers;
}

// generate a brief report
// if showAnswer is true, display questions solved with correct answers
//                 otherwise, display questions solved without answers
void MathReport::generateReport(bool showAnswer) const
{
    cout << "You have solved the following 4 math problems: " << endl;
    for(int i = 0; i < mathQuestions.size(); i++){
        mathQuestions[i].print();
        if(showAnswer){
            cout <<  setw(5) << mathQuestions[i].getAnswer() << endl;
        }
        cout << endl;
    }
    cout << "----------------------------------" << endl;
    cout << "You answered " << numCorrectAnswers << " questions correctly." << endl;
    if(numCorrectAnswers > numWrongAnswers){
        cout << "You made " << numWrongAnswers << " mistakes." << endl;
        cout << "You will do better next time. " << endl;
    }
    else{
        cout << "You made " << numWrongAnswers << " mistakes." << endl;
        cout << "Great job!" << endl;
    }
}

// display the questions in errorList for practice again and collect the user answer
// then check if the answer is correct so that it can be removed from the errorList
// it returns false if all questions in errorList have been corrected and removed from the errorList
// otherwise returns true: errorList is not empty yet, need more practice
bool MathReport::needMorePractice()
{
    list<MathOperations>::iterator pos;
    for(pos = errorList.begin(); pos != errorList.end(); pos++){
        cout << "Please type your answer: " << endl;
        int userInput = (*pos).collectUserAnswer();
        if(userInput == (*pos).getAnswer()){
            cout << "Congratulations! " << (*pos).getAnswer() << " is the right answer." << endl;
            pos = errorList.erase(pos);
            pos--;
            numCorrectAnswers++;
            numWrongAnswers--;
        }
        else{
            cout << "Sorry, the answer is wrong. You may practice again." << endl;
        }
    }
    int count = 0;
    for(pos = errorList.begin(); pos != errorList.end(); pos++){
        count++;
    }
    return (count != 0);
}
