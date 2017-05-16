This plugin provides currency conversion
through the free JSON API at free.currencyconverterapi.com.

Their free API allows a maximum of 100 requests per hour from the same
IP address. Their exchange rates are updated every 30 minutes.
Since a list of all exchange rates cannot be retrieved in a single query,
the plugin makes an effort to cache the exchange rates for some time
(30 minutes by default, but this can be adjusted with the `refreshInterval`
configuration variable) to reduce the amount of requests to the API.
This means that, for example, if you convert between USD and EUR,
the exchange rate from USD to EUR and the reverse (EUR to USD) will be cached,
and if another conversion is made within the refresh interval,
it won't be re-requested from the API. This cache will also be cleared
if you reload the plugin or restart the bot.
