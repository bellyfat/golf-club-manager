from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class GameTest(FunctionalTest):

    def test_can_record_Stroke_game(self):
        # Bob has just finished playing a round of golf with the club and has
        # to get everyone's new handicap
        self.browser.get(self.live_server_url)

        # He navigates to the Record a game page
        self.browser.find_element_by_link_text('Record a game').click()

        # It makes him log in
        self.login()

        # He waits for the page to load and then starts filling in the form
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Record a game"
        ))

        self.replace_value_in_form('id_game_date', '07/29/2017')

        self.choose_dropdown_item('id_game_type', 'Stroke')

        self.replace_value_in_form('id_form-0-score', '74')
        self.replace_value_in_form('id_form-3-score', '72')
        self.replace_value_in_form('id_form-5-score', '70')
        self.replace_value_in_form('id_form-7-score', '69')

        self.browser.find_element_by_tag_name("button").click()

        # He notices the Players page then reloads and he can see that
        # the players scores have adjusted
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Players"
        ))

        self.check_values_in_table(
            "id_player_table",
            "Abbott, Tony - Edit 18.3 18 2017-07-29 0.3",
            "tr"
        )
        self.check_values_in_table(
            "id_player_table",
            "Chifley, Ben - Edit 18.5 18 2017-07-29 -0.5",
            "tr"
        )
        self.check_values_in_table(
            "id_player_table",
            "Curtin, John - Edit 40.0 40 2017-07-29 -1.0",
            "tr"
        )
        self.check_values_in_table(
            "id_player_table",
            "Dudd, Kevin - Edit 25.0 25 2017-07-29 -2.0",
            "tr"
        )

    def test_can_record_Stableford_game(self):
        # Bob has just finished playing a round of golf with the club and has
        # to get everyone's new handicap
        self.browser.get(self.live_server_url)

        # He navigates to the Record a game page
        self.browser.find_element_by_link_text('Record a game').click()

        # It makes him log in
        self.login()

        # He waits for the page to load and then starts filling in the form
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Record a game"
        ))

        self.replace_value_in_form('id_game_date', '06/20/2017')

        self.choose_dropdown_item('id_game_type', 'Stableford')

        self.replace_value_in_form('id_form-0-score', '41')
        self.replace_value_in_form('id_form-3-score', '39')
        self.replace_value_in_form('id_form-5-score', '37')
        self.replace_value_in_form('id_form-7-score', '36')

        self.browser.find_element_by_tag_name("button").click()

        # He notices the Players page then reloads and he can see that
        # the players scores have adjusted
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Players"
        ))

        self.check_values_in_table(
            "id_player_table",
            "Abbott, Tony - Edit 16.0 16 2017-06-20 -2.0",
            "tr"
        )
        self.check_values_in_table("id_player_table",
            "Chifley, Ben - Edit 18.0 18 2017-06-20 -1.0",
            "tr"
        )
        self.check_values_in_table(
            "id_player_table",
            "Curtin, John - Edit 40.5 40 2017-06-20 -0.5",
            "tr"
        )
        self.check_values_in_table(
            "id_player_table",
            "Dudd, Kevin - Edit 27.3 27 2017-06-20 0.3",
            "tr"
        )


class GameTypeTest(FunctionalTest):

    def test_can_view_game_types(self):
        # Bob wants to add a new game type called Stringball
        self.browser.get(self.live_server_url)

        # He looks at the available content and eventually clicks the Settings
        # button
        self.browser.find_element_by_link_text('Settings').click()

        # Bob is then presented with the existing game types
        game_types = self.browser.find_elements_by_class_name(
            'settings-list-title')
        self.assertIn('Stableford', [types.text for types in game_types])
        self.assertIn('Stroke', [types.text for types in game_types])
        self.assertNotIn('Stringball', [types.text for types in game_types])

    def test_can_create_new_game_type(self):
        # Bob wants to add a new game type called Stringball
        self.browser.get(self.live_server_url)

        # He looks at the available content and eventually clicks the Settings
        # button
        self.browser.find_element_by_link_text('Settings').click()

        # Bob clicks the button to add a new game type. He is prompted to log in
        self.browser.find_element_by_link_text('Add New Game Type').click()

        self.login()

        # Upon successfully logging in he sees that the correct page has loaded
        # and starts filling in the rules
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Add New Game Type"
        ))

        self.replace_value_in_form('id_name', 'Stringball')
        self.replace_value_in_form('id_level_4', '10')
        self.replace_value_in_form('id_level_4_result', '0.3')
        self.replace_value_in_form('id_level_3_min', '11')
        self.replace_value_in_form('id_level_3_max', '12')
        self.replace_value_in_form('id_level_3_result', '-0.5')
        self.replace_value_in_form('id_level_2_min', '13')
        self.replace_value_in_form('id_level_2_max', '14')
        self.replace_value_in_form('id_level_2_result', '-1.0')
        self.replace_value_in_form('id_level_1', '15')
        self.replace_value_in_form('id_level_1_result', '-2')
        self.browser.find_element_by_tag_name("button").click()

        # The page reloads and Bob sees his game type in the list
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Settings"
        ))
        game_types = self.browser.find_elements_by_class_name(
            'settings-list-title')
        self.assertIn('Stringball', [types.text for types in game_types])

    def test_can_edit_game_type(self):
        # Bob wants to rename the Stableford game type to Stringball
        self.browser.get(self.live_server_url)

        # He clicks the settings button
        self.browser.find_element_by_link_text('Settings').click()

        # Bob clicks the Edit button next to Stableford.
        # He is prompted to log in
        self.browser.find_element_by_id('edit-Stableford').click()

        self.login()

        # Upon successfully logging in he sees that the correct page has loaded
        # and renames the game type
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Edit Game Type"
        ))

        self.replace_value_in_form('id_name', 'Stringball')
        self.browser.find_element_by_tag_name('button').click()

        # The page reloads and Bob sees his game type in the list
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Settings"
        ))
        game_types = self.browser.find_elements_by_class_name(
            'settings-list-title')
        self.assertIn('Stringball', [types.text for types in game_types])
        self.assertNotIn('Stableford', [types.text for types in game_types])