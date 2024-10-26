.PHONY: flood
flood:
	@python network_protocols/main.py flood

.PHONY: leach
leach:
	@python network_protocols/main.py leach

.PHONY: funnel
funnel:
	@python network_protocols/main.py funnel

.PHONY: test
test:
	@pytest