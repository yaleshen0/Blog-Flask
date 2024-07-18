"""
This file (test_cli.py) contains the functional tests for the CLI (Command-Line Interface) functions.
"""

def test_initialize_database(cli_test_client):
    """
    Given a Flask application configured for testing
    When the 'flask init_db' command is called from the command line
    Then check the response is valid
    """
    output = cli_test_client.invoke(args=['init_db'])
    assert output.exit_code == 0
    assert 'Database initialized' in output.output
