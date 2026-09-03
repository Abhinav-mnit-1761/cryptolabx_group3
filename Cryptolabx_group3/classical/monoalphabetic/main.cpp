#include <iostream>
#include <fstream>
#include "substitution.h"

using namespace std;

int main()
{
    ifstream file("../../datasets/plaintext.txt");

    if (!file)
    {
        cout << "Error opening plaintext file." << endl;
        return 1;
    }

    string plaintext;
    string line;

    while (getline(file, line))
    {
        plaintext += line + "\n";
    }

    file.close();

    string key = "QWERTYUIOPASDFGHJKLZXCVBNM";

    string ciphertext = encrypt(plaintext, key);
    
    
    frequency_analysis(ciphertext);
    
    word_frequency_analysis(ciphertext);
    
    pattern_analysis(ciphertext);
    

    ofstream output("../../outputs/monoalpha_ciphertext.txt");

    if (!output)
    {
        cout << "Error creating ciphertext file." << endl;
        return 1;
    }

    output << ciphertext;

    output.close();

    cout << "Encryption completed successfully." << endl;
    cout << "Ciphertext saved to outputs/monoalpha_ciphertext.txt" << endl;
    
    string partial_key = "??????????????????????????";

    while (true)
	{
	    char cipher_letter;
	    char plain_letter;
	    char choice;

	    cout << "\nEnter substitution (cipher plaintext), or 0 0 to stop: ";
	    cin >> cipher_letter >> plain_letter;

	    if (cipher_letter == '0' && plain_letter == '0')
		break;

	    cipher_letter = toupper(cipher_letter);
	    plain_letter = toupper(plain_letter);

	    if (!valid_substitution(partial_key, cipher_letter, plain_letter))
	    {
		cout << "Invalid substitution." << endl;
		continue;
	    }

	    // Try the substitution temporarily
	    string test_key = partial_key;

	    test_key[cipher_letter - 'A'] = plain_letter;

	    string partial_plaintext =
		apply_substitution(ciphertext, test_key);

	    display_partial_plaintext(partial_plaintext);

	    cout << "\nAccept substitution? (y/n): ";
	    cin >> choice;

	    if (choice == 'y' || choice == 'Y')
	    {
		partial_key = test_key;
		cout << "Substitution accepted." << endl;
	    }
	    else
	    {
		cout << "Substitution rejected." << endl;
	    }
	}
	

    return 0;
}
