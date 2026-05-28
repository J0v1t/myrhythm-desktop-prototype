import pytest
import json
from unittest.mock import patch, MagicMock

pytest.importorskip("sqlalchemy")

from app.logic.preferences_logic import save_user_preferences, load_user_preferences, reset_user_preferences

class TestPreferencesLogic:
    @patch('app.logic.preferences_logic.db')
    @patch('app.logic.preferences_logic.UserPreferences')
    def test_save_user_preferences_new(self, mock_UserPreferences, mock_db):
        mock_session = MagicMock()
        mock_db.session = mock_session

        # Mock that no existing preferences exist
        mock_UserPreferences.query.filter_by.return_value.first.return_value = None
        mock_prefs = MagicMock()
        mock_UserPreferences.return_value = mock_prefs

        result = save_user_preferences(1, ['rock', 'jazz'], ['artist1', 'artist2'], {'happy': 'upbeat'})

        assert result == mock_prefs
        mock_session.add.assert_called_once_with(mock_prefs)
        mock_session.commit.assert_called_once()
        assert mock_prefs.favorite_genres == 'rock,jazz'
        assert mock_prefs.favorite_artists == 'artist1,artist2'
        assert mock_prefs.mood_mapping == json.dumps({'happy': 'upbeat'})

    @patch('app.logic.preferences_logic.db')
    @patch('app.logic.preferences_logic.UserPreferences')
    def test_save_user_preferences_existing(self, mock_UserPreferences, mock_db):
        mock_session = MagicMock()
        mock_db.session = mock_session

        mock_existing_prefs = MagicMock()
        mock_UserPreferences.query.filter_by.return_value.first.return_value = mock_existing_prefs

        result = save_user_preferences(1, ['pop'], ['artist3'], {'sad': 'slow'})

        assert result == mock_existing_prefs
        mock_session.add.assert_called_once_with(mock_existing_prefs)
        mock_session.commit.assert_called_once()
        assert mock_existing_prefs.favorite_genres == 'pop'
        assert mock_existing_prefs.favorite_artists == 'artist3'
        assert mock_existing_prefs.mood_mapping == json.dumps({'sad': 'slow'})

    @patch('app.logic.preferences_logic.UserPreferences')
    def test_load_user_preferences_existing(self, mock_UserPreferences):
        mock_prefs = MagicMock()
        mock_prefs.favorite_genres = 'rock,jazz'
        mock_prefs.favorite_artists = 'artist1,artist2'
        mock_prefs.mood_mapping = json.dumps({'happy': 'upbeat'})
        mock_UserPreferences.query.filter_by.return_value.first.return_value = mock_prefs

        result = load_user_preferences(1)

        expected = {
            "genres": ['rock', 'jazz'],
            "artists": ['artist1', 'artist2'],
            "mood_map": {'happy': 'upbeat'}
        }
        assert result == expected

    @patch('app.logic.preferences_logic.UserPreferences')
    def test_load_user_preferences_none(self, mock_UserPreferences):
        mock_UserPreferences.query.filter_by.return_value.first.return_value = None

        result = load_user_preferences(1)

        expected = {"genres": [], "artists": [], "mood_map": {}}
        assert result == expected

    @patch('app.logic.preferences_logic.db')
    @patch('app.logic.preferences_logic.UserPreferences')
    def test_reset_user_preferences_existing(self, mock_UserPreferences, mock_db):
        mock_session = MagicMock()
        mock_db.session = mock_session

        mock_prefs = MagicMock()
        mock_UserPreferences.query.filter_by.return_value.first.return_value = mock_prefs

        result = reset_user_preferences(1)

        assert result is True
        mock_session.delete.assert_called_once_with(mock_prefs)
        mock_session.commit.assert_called_once()

    @patch('app.logic.preferences_logic.db')
    @patch('app.logic.preferences_logic.UserPreferences')
    def test_reset_user_preferences_none(self, mock_UserPreferences, mock_db):
        mock_session = MagicMock()
        mock_db.session = mock_session

        mock_UserPreferences.query.filter_by.return_value.first.return_value = None

        result = reset_user_preferences(1)

        assert result is False
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()
