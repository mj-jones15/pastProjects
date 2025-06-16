#include "MathOperations.h"
#include <iomanip>
//Default constructor
MathOperations::MathOperations()
{
}
// set the private data members: operand1 and operand2
// to op1 and op2 respectively
void MathOperations::setOperands(int op1, int op2)
{
    operand1 = op1;
    operand2 = op2;
}

// get the current value of the private data member: theoperator
char MathOperations::getOperator() const
{
    return theoperator;
}
// return the value of the data member: answer
int MathOperations::getAnswer() const
{
    return answer;
}
// set theoperator to '+'
// apply the addition operation to operand1 and operand2
// set the answer equal to operand1 + operand2
void MathOperations::Addition()
{
    theoperator = '+';
    answer = operand1 + operand2;
}
// set theoperator to '-'
// apply the subtraction operation to operand1 and operand2
// set the answer equal to operand1 - operand2
void MathOperations::Subtraction()
{
    theoperator = '-';
    answer = operand1 - operand2;
}
// set theoperator to '*'
// apply the multiplication operation to operand1 and operand2
// set the answer equal to operand1 * operand2
void MathOperations::Multiplication()
{
    theoperator = '*';
    answer = operand1 * operand2;
}
// set theoperator to const DivisionSymbol, it is ASCII code for obelus
// apply the division operation to operand1 and operand2
// set the answer equal to operand1 ÷ operand2
void MathOperations::Division()
{
    theoperator = DivisionSymbol;
    answer = operand1 / operand2;
}
// if answer == response, it returns true
// otherwise it returns false
bool MathOperations::checkAnswer(int response) const
{
    return (answer == response);
}
//display the question in the format described in the problem statement
// for example:
//    135
//  +  78
//  _____
//
void MathOperations::print() const
{
    cout << setw(5) << operand1 << endl;
    cout << theoperator << setw(4) << operand2 << endl;
    cout <<"-----" << endl;
}
// display the question by calling print() first
// then ask the user for the answer
// it returns the valid user answer collected from the user input 
int MathOperations::collectUserAnswer() const
{
    print();
    int userInput;
    bool isValid = false;
    while(!isValid){
        cout << "Please type your answer: " << endl;
        cin >> userInput;
        if(cin.fail()){
            cin.clear();
            cin.ignore(256, '\n');
            cout << "Invalid input. Please try again." << endl;
        }
        else{
            isValid = true;
        }
    }
    return userInput;
}
