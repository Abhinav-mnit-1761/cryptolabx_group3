#include <iostream>
#include "substitution.h"
#include <cctype>
#include <vector>

string encrypt(const string& plaintext, const string& key)
{
    string ciphertext = plaintext;

    for (int i = 0; i < plaintext.length(); i++)
    {
        if (isupper(plaintext[i]))
        {
            ciphertext[i] = key[plaintext[i] - 'A'];
        }
        else if (islower(plaintext[i]))
        {
            ciphertext[i] = tolower(key[plaintext[i] - 'a']);
        }
    }

    return ciphertext;
}

string decrypt(const string& ciphertext, const string& key)
{
    string plaintext = ciphertext;

    for (int i = 0; i < ciphertext.length(); i++)
    {
        if (isupper(ciphertext[i]))
        {
            for (int j = 0; j < 26; j++)
            {
                if (key[j] == ciphertext[i])
                {
                    plaintext[i] = 'A' + j;
                    break;
                }
            }
        }
        else if (islower(ciphertext[i]))
        {
            for (int j = 0; j < 26; j++)
            {
                if (tolower(key[j]) == ciphertext[i])
                {
                    plaintext[i] = 'a' + j;
                    break;
                }
            }
        }
    }

    return plaintext;
}


void frequency_analysis(const string& ciphertext)
{
    int frequency[26] = {0};
    int total_letters = 0;

    // Count each letter
    for (int i = 0; i < ciphertext.length(); i++)
    {
        if (isupper(ciphertext[i]))
        {
            frequency[ciphertext[i] - 'A']++;
            total_letters++;
        }
        else if (islower(ciphertext[i]))
        {
            frequency[ciphertext[i] - 'a']++;
            total_letters++;
        }
    }

    // Store letter indexes
    int order[26];

    for (int i = 0; i < 26; i++)
    {
        order[i] = i;
    }

    // Sort indexes by frequency
    for (int i = 0; i < 25; i++)
    {
        int max_index = i;

        for (int j = i + 1; j < 26; j++)
        {
            if (frequency[order[j]] > frequency[order[max_index]])
            {
                max_index = j;
            }
        }

        int temp = order[i];
        order[i] = order[max_index];
        order[max_index] = temp;
    }

    // Display results
    cout << "\nLetter Frequency Analysis\n";
    cout << "-------------------------\n";

    for (int i = 0; i < 26; i++)
    {
        int letter = order[i];

        double percentage = (frequency[letter] * 100.0) / total_letters;

        cout << char('A' + letter)
             << " : "
             << frequency[letter]
             << " ("
             << percentage
             << "%)\n";
    }
}

void word_frequency_analysis(const string& ciphertext)
{
    vector<string> words;
    string word = "";

    for (int i = 0; i <= ciphertext.length(); i++)
    {
        if (isalpha(ciphertext[i]))
        {
            word += tolower(ciphertext[i]);
        }
        else
        {
            if (!word.empty())
            {
                words.push_back(word);
                word = "";
            }
        }
    }

    cout << "\nRepeated Words\n";
    cout << "--------------\n";

    for (int i = 0; i < words.size(); i++)
    {
        int count = 1;

        for (int j = i + 1; j < words.size(); j++)
        {
            if (words[i] == words[j])
                count++;
        }

        bool already_displayed = false;

        for (int j = 0; j < i; j++)
        {
            if (words[i] == words[j])
            {
                already_displayed = true;
                break;
            }
        }

        if (!already_displayed && count > 1)
        {
            cout << words[i] << " : " << count << endl;
        }
    }

    cout << "\nOne-letter Words\n";
    cout << "----------------\n";

    for (int i = 0; i < words.size(); i++)
    {
        if (words[i].length() == 1)
            cout << words[i] << endl;
    }

    cout << "\nTwo-letter Words\n";
    cout << "----------------\n";

    for (int i = 0; i < words.size(); i++)
    {
        if (words[i].length() == 2)
            cout << words[i] << endl;
    }

    cout << "\nThree-letter Words\n";
    cout << "------------------\n";

    for (int i = 0; i < words.size(); i++)
    {
        if (words[i].length() == 3)
            cout << words[i] << endl;
    }
}

string get_pattern(const string& word)
{
    string pattern = "";
    int next_number = 0;

    for (int i = 0; i < word.length(); i++)
    {
        int number = -1;

        for (int j = 0; j < i; j++)
        {
            if (word[i] == word[j])
            {
                number = pattern[j] - '0';
                break;
            }
        }

        if (number == -1)
        {
            number = next_number;
            next_number++;
        }

        pattern += char('0' + number);
    }

    return pattern;
}

void pattern_analysis(const string& ciphertext)
{
    vector<string> words;
    string word = "";

    for (int i = 0; i <= ciphertext.length(); i++)
    {
        if (isalpha(ciphertext[i]))
        {
            word += tolower(ciphertext[i]);
        }
        else
        {
            if (!word.empty())
            {
                words.push_back(word);
                word = "";
            }
        }
    }

    cout << "\nWord Pattern Analysis\n";
    cout << "---------------------\n";

    for (int i = 0; i < words.size(); i++)
    {
        cout << words[i]
             << " : "
             << get_pattern(words[i])
             << endl;
    }
}


string apply_substitution(const string& ciphertext, const string& key)
{
    string plaintext = ciphertext;

    for (int i = 0; i < ciphertext.length(); i++)
    {
        if (isupper(ciphertext[i]))
        {
            int index = ciphertext[i] - 'A';

            if (key[index] != '?')
                plaintext[i] = key[index];
            else
                plaintext[i] = '_';
        }
        else if (islower(ciphertext[i]))
        {
            int index = ciphertext[i] - 'a';

            if (key[index] != '?')
                plaintext[i] = tolower(key[index]);
            else
                plaintext[i] = '_';
        }
    }

    return plaintext;
}

void display_partial_plaintext(const string& plaintext)
{
    cout << "\nPartial Plaintext\n";
    cout << "-----------------\n";
    cout << plaintext << endl;
}

bool valid_substitution(const string& key, char cipher_letter, char plain_letter)
{
    int cipher_index = toupper(cipher_letter) - 'A';
    plain_letter = toupper(plain_letter);

    for (int i = 0; i < 26; i++)
    {
        if (i != cipher_index && key[i] == plain_letter)
            return false;
    }

    return true;
}

string frequency_substitution(const string& ciphertext)
{
    int frequency[26] = {0};

    // Frequency analysis
    for (int i = 0; i < ciphertext.length(); i++)
    {
        if (isalpha(ciphertext[i]))
        {
            frequency[toupper(ciphertext[i]) - 'A']++;
        }
    }

    // Store letter positions
    int order[26];

    for (int i = 0; i < 26; i++)
    {
        order[i] = i;
    }

    // Sort by frequency
    for (int i = 0; i < 25; i++)
    {
        int max_index = i;

        for (int j = i + 1; j < 26; j++)
        {
            if (frequency[order[j]] > frequency[order[max_index]])
            {
                max_index = j;
            }
        }

        int temp = order[i];
        order[i] = order[max_index];
        order[max_index] = temp;
    }

    // English letter frequency order
    string english_frequency = "ETAOINSHRDLCUMWFGYPBVKJXQZ";

    // Replace ciphertext letters
    string result = ciphertext;

    for (int i = 0; i < ciphertext.length(); i++)
    {
        if (isupper(ciphertext[i]))
        {
            for (int j = 0; j < 26; j++)
            {
                if (order[j] == ciphertext[i] - 'A')
                {
                    result[i] = english_frequency[j];
                    break;
                }
            }
        }
        else if (islower(ciphertext[i]))
        {
            for (int j = 0; j < 26; j++)
            {
                if (order[j] == ciphertext[i] - 'a')
                {
                    result[i] = tolower(english_frequency[j]);
                    break;
                }
            }
        }
    }
    return result;
}

bool verify_solution(const string& plaintext,
                     const string& ciphertext,
                     const string& key)
{
    string regenerated_ciphertext = encrypt(plaintext, key);

    if (regenerated_ciphertext == ciphertext)
        return true;

    return false;
}
