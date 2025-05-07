## Functional Requirements
---------------------------------------------------------------------------------------------------------------
1. User Registration
A visitor can create an account by providing a username, email, and password.
2. User Login
Registered users can log in using their email and password.
3. User Logout
Logged-in users can securely log out of their account.
4. Create Recipe
Logged-in users can add new recipes with a title, description, ingredients, and
instructions.
5. Edit Recipe
Users can update their own recipes after they have been created.
6. Delete Recipe
Users can delete recipes that they have created.
7. View Recipe
Anyone (logged-in or not) can view the details of a recipe including ingredients and
instructions.
8. Search Recipe
Users can search for recipes by title or keywords (e.g., ingredients).
9. Rate Recipe
Users can rate recipes on a scale from 1 to 5 stars.
10.Comment on Recipe
Users can leave comments on recipes to provide feedback or ask questions.
11.View User Profile
Users can view their own profile, including submitted recipes.
12.Edit User Profile
Users can update their profile details, including display name, email, and password.
13.Save Recipe (Favorites)
Users can save or "favorite" recipes to access them more easily later.
14.View All Recipes
The homepage or main recipe list will display all recipes stored in the database.
15.Filter Recipes
Users can filter recipes by predefined tags such as 'vegan', 'dessert', or 'gluten-free'.

## Non-functional Requirements
---------------------------------------------------------------------------------------------------------------
1. Pages load within 1 second
2. The password database is secured by any type of encryption
3. xxx
## Use Cases
---------------------------------------------------------------------------------------------------------------
1. User Registration
Actors: are the users attempting to register!
User Registration
Description: A visitor can create an account by providing a username, email, and
password.
Preconditions: the User must have an email address, as well as a computer/phone!
Main Flow:
1. The user will input their email address and decide on a password they will use.
2. They will input that password, and this created a user login for them!
Alternate Flows: If a user inputs an email associated with another account already, there
will be an email in use error! If the password is not valid, it will output an error telling you
so! If you try to continue without inputting anything, it will output that you need to fill
these fields!
Postconditions: There needs to be a database that has everyone’s login info saved away so
there are no duplicate accounts, and that their information can be saved in the first place!
---------------------------------------------------------------------------------------------------------------
2. User Login
Actors: The Users attempting to login!
User Login
Description: Registered users can log in using their email and password.
Preconditions: The user must have made an account prior, and be inputting their info
correctly! The User needs to be alive and have access to a computer/mobile.
Main flow:
1. The user will input their email & password into their respective fields,
2. then they press login & are redirected to the next page!
Alternate flows: If a user inputs the wrong email or password, they will be output an error
saying so! If the user doesn’t fill in anything, they will be issued an error telling them to do
so!
Postconditions: There needs to be a valid database to insure they are logged in to the
correct account, and for the servers hosting the website are online
---------------------------------------------------------------------------------------------------------------
3. User Logout
Actors: The users that are logged in
User Logout
Description: Logged-in users can log out of their account securely.
Preconditions: That the user was logged in in the first place!
Main flow:
1. The user will move their cursor to the top right & locate the logout button.
2. Once they find the button, they click it and they get redirected to the home page
without being logged in.
Alternate flow: If the user is in the middle of editing information & attempts to log out,
they will receive a message saying “finish doing what you’re doing, then log out!”
Postconditions: That there is a redirection to the home page once you log out! The servers
need to be online to host the page itself!
---------------------------------------------------------------------------------------------------------------
4. Create Recipe
Actors: the Users of the website interested in posting recipes.
Create Recipe
Description: Logged-in users can add new recipes with title, description, ingredients, and
instructions.
Preconditions: That the user is logged in!
Main flow:
1. The user will navigate to the create recipe page.
2. There they will fill out all the required information relevant to their recipe.
3. Once they’ve filled it out, they’ll click enter and their recipe will be saved/posted
online!
Alternate flow: If the use is not logged in, they will receive an error telling them to login
first! If the use does not fill out the required fields, they will receive an error saying they
must fill out all the required fields before continuing!
Postconditions: The server hosting the website is online, and the database holding all the
recipes correctly records it and runs as it is supposed to!
---------------------------------------------------------------------------------------------------------------
5. Edit Recipe
Actors: The users with a recipe to edit.
Edit Recipe
Description: Users can update their own recipes after creation.
Preconditions: That there is a recipe they created earlier that they can edit, & that they’re
logged in.
Main flow:
1. The user will click the edit recipe button under a recipe that they have created.
2. Once in, they will change any fields they would like to, and then press save!
3. The new recipe will reflect the changes they made.
Alternate flow: If the user is not logged in, they will be told to login before they can access
that page. If the user is attempting to edit someone else’s recipe, they will be given an
error saying they can not. If they put in foul language, they will be prompted to change
their input.
Postconditions: The database correctly updates the information of the correct recipe.
---------------------------------------------------------------------------------------------------------------
6. Name: Delete Recipe
Summary: Users can delete their own recipes.
Actors: Users, System
Pre-Conditions: User has logged in, wants to edit their recipe(delete), is on the desired
recipe page.
Trigger: User selects delete recipe
Primary Sequence:
1. User clicks edit recipe
2. System prompts message on whether to edit, delete, or cancel
3. User selects delete
4. System provides confirmation
5. User confirms deletion
6. System removes recipe from database
Alternative Sequence:
User clicks edit recipe
System prompts message on whether to edit, delete, or cancel
User selects cancel
System removes the edit prompt
Post Condition:
The user removes the recipe from their account
or
The User cancels deleting the recipe and the recipe stays
---------------------------------------------------------------------------------------------------------------
7. Name: View Recipe
Summary: Anyone can view the details of a recipe including ingredients and instructions.
Actors: Users, System
Pre-Conditions: User has logged in, wants to view their recipe, User is on the main page
where all the recipes are listed
Trigger: User selects on their recipe
Primary Sequence:
1. System displays list of recipes
2. User clicks on the desired recipe
3. System redirects to the recipe page
4. System prompts the recipe and its entirety
Alternative Sequence:
System displays list of recipes
User clicks on back
System redirects to the recipe page and displays their saved recipes
Post Condition:
The user is able to view their recipe
or
The user views their recipe and decides to go back and look at other recipes
---------------------------------------------------------------------------------------------------------------
8. Name: Search Recipe
Summary: Users can search recipes by title or ingredient keywords.
Actors: Users, System
Pre-Conditions: User has logged in, wants to search for a specific recipe.
Trigger: User logs clicks on recipes button
Primary Sequence:
1. System displays list of recipes
2. User clicks on the search button at the top of the page
3. System displays search bar UI with instructions on how to search
4. User inputs keywords suggested by the UI
5. System compares keywords with search keys from the recipes
6. System forwards to the searched recipe page
Alternative Sequence:
Recipe isn’t found by system
System displays No recipe found
Multiple recipe found by system
System displays a list of recipes
User searches for another recipe and System brings up UI
Post Condition:
User is redirected to recipe page
or
System displays multiple recipes allowing for users to select desired recipe
or
System displays no recipes and lets the user know
---------------------------------------------------------------------------------------------------------------
9. Rate Recipe
Users can rate a recipe from 1 to 5 stars.
Actors: Users, System
Pre-Conditions: User has logged in, wants to rate their/others recipe, is on the desired
recipe page,
Trigger: User selects on a recipe
Primary Sequence:
1. User clicks on rate
2. System prompts an interactive menu with integers ranging from 1-5
3. User clicks on one of the 5 selections to rate recipe
4. System saves the rating
5. System displays rating
Alternative Sequence:
User searches for another recipe and System brings up UI
User doesn’t want to rate the recipe
Post Condition:
User successfully rates the recipe
or
User decided not to rate recipe and is redirected back to the recipe
---------------------------------------------------------------------------------------------------------------
10. Comment on Recipe
Users can leave comments on a recipe.
Actors: Users, System
Pre-Conditions: User has logged in, wants to rate their/others recipe, user is on desired
recipe.
Trigger: User selects on a recipe
Primary Sequence:
User clicks on comment
1. System prompts an interactive menu telling the user to leave a comment
2. User inputs desired comment
3. System saves the comments
4. System display the comment
Alternative Sequence:
User doesn’t want to comment
System then redirects back to recipe page
Post Condition:
User successfully comments on the recipe
or
User is redirected back to the recipe page after canceling the comment
---------------------------------------------------------------------------------------------------------------
11. View User Profile
Users can view their own profile, including their submitted recipes.
Use Case Name: View User Profile
Pre-Condition: User is logged in and registered
Trigger: User presses on button labelled view profile
Primary Sequence:
1. User clicks on “View Profile”
2. System retrieves information relating to the creation of the user and the
name/email of the user
3. System retrieves any submitted recipes that the user has submitted
4. Route to a webpage in which the user can view the information relating to their
user and can view a list of all the recipes that they have submitted
Primary Post-Conditions: User has access to the page that displays all the
information relating to their own user and can view the different recipes that they may
have submitted.
Alternate Sequence: User is not logged in
User attempts to click on “View Profile”
Redirect user to sign in page
Generate the user’s profile as seen above
Alternate Sequence: User has no Recipes
User clicks on “View Profile”
System retrieves information relating to the user
Profile Page Displays text “No Submitted Profiles”
Display button allowing user to navigate to the “Submit Recipe” page
---------------------------------------------------------------------------------------------------------------
12. Edit User Profile
Users can update their display name, email, or password.
Use Case Name: Edit User Profile
Pre-Condition: User is logged in and is a registered user
Trigger: User clicks on “Edit Profile” button on the user profile page
Primary Sequence:
1. Direct user to “Edit Profile” page
2. System displays current profile page
3. User edits profile name, email, password
4. User presses a button labelled “Save Profile”
5. System writes changes to User Data Base to save the changes
6. Redirect User to newly edited Profile Page
Primary Post Conditions: User has been able to edit their profile page and was able
to edit their display name, email address associated with profile, and password.
Alternate Sequence: User does not save profile
Prompt user that they are navigating away from unsaved web page
User continues to exit page without saving
System disregards any changes made within the profile page
System does not update the database with any new information
---------------------------------------------------------------------------------------------------------------
13. Save Recipe (Favorites)
Users can save or 'favorite' recipes for quick access later.
Use Case Name: User saves recipe for later
Pre-Condition: User is logged in and is viewing a recipe
Trigger: User clicks on button labelled “Favourite Recipe”
Primary Sequence:
1. Prompt User with a confirm favorite recipe button
2. System saves currently viewed recipe to the user’s “Favorite Recipes” list/structure
3. Display “Recipe Saved” on webpage when recipe is successfully saved
Primary Post Conditions: Recipe the user wanted to favorite is saved in the
database to the user’s account in some way. Newly favorited recipe is viewable from
Profile Page or Favorite Recipe Page
Alternate Sequence: User does not confirm
User navigates to another page without confirming they wanted to save the recipe
System does not save the recipe to the User database
Alternate Sequence: User is not logged in
Redirect User to login Page
User logs in
Redirect User to the Recipe they were looking at
Perform Primary Sequence
---------------------------------------------------------------------------------------------------------------
14. View All Recipes
Homepage or main recipe list shows all recipes available in the database.
Use Case Name: View All Recipes
Pre-Condition: Website is running
Trigger: A user is viewing homepage / main recipe list
Primary Sequence:
1. User navigates to homepage
2. System retrieves all recipes within the database
3. System displays all recipes in an ordered list from most recent to oldest
a. Primary Post Conditions: User is able to view and navigate through all the
recipes currently stored within the data base
b. Alternate Sequence: No recipes in the database
4. System attempts to retrieve all recipes within the database
5. If none are found display text “No Recipes Found”
6. Display button that allows user to submit their own recipe
---------------------------------------------------------------------------------------------------------------
15. Filter Recipes
Users can filter recipes by tags like 'vegan', 'dessert', etc.
Use Case Name: Filter Recipes
Pre-Condition: User is viewing the main homepage or all recipes page
Trigger: User clicks on a tag containing some sort of filter
Primary Sequence:
1. System sorts through the list of recipes
2. System retrieves all recipes associated with the filter the user requested
3. System displays all recipes that were retrieved from the tag
Primary Post Condition: All recipes associated with the filter tags that the user
requested are viewable by the user
Alternate Sequence: No recipes found under requested filter
System attempts to retrieve all recipes with the filter the user requested
Display text “No Recipe Found with Current Filter”
