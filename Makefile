IMAGE := fedora:29

run-in-container:
	podman run --rm -ti \
		-e GITHUB_TOKEN \
		-v $(CURDIR):/src:Z \
		-w /src \
		$(IMAGE) \
		bash -c "\
			dnf install -y git-core \
			&& pip3 install . \
			&& show-me \
		"
