Given i have a cool gherkin quality checker
When i parse this scenario
Then i expect a positive result

Given i have a cool gherkin quality checker
When i parse this scenario
And add another
And add another
Then i expect a positive result
And pass me a warning for too long

Given i have a cool gherkin quality checker
When i parse this scenario
And add another
And add another
And add another
Then i expect a negative result
And pass me the failing errors

Given i have a cool gherkin quality checker
When i parse this scenario
And add another
And add another
Or add another
Then i expect a negative result
And pass me the failing errors

Given i have this gherkin
And i run the gherkin quality checker
When i parse this scenario
Then i expect this to fail
And pass me the failing error

Given i have this gherkin
When i parse this scenario
And refer to myself (I/We) and not to a proper user
Then i expect this to warn me
And pass me a warning

Given i have this gherkin
When i parse this scenario
And pass only <one> example
Then i expect this to warn me
And pass me a warning
	Examples:
	|one|
	|one|

Given i have a cool gherkin quality checker
When i parse this file
Then i expect a total quality score