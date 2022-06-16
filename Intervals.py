import intervals as I

# k core decomp(G)
# sol = I.closed(R(G) + len(deleted_nodes) + sum(ingrad(deleted_nodes)) , R(G) + x * (n-x+1))

# if sol in aktuell --> aktuell ist definitiv besser wenn sol.lower > aktuell.upper. sonst ist sol besser
# if sol not in aktuell --> if sol <= aktuell --> sol ist definitiv besser
# if sol not in aktuell --> if sol >= aktuell --> aktuell ist definitiv besser
# if sol not in aktuell --> if sol.lower < aktuell.lower and sol.upper > aktuell.upper --> aktuell oder sol
# möglichkeit 1 : Differenz messen
