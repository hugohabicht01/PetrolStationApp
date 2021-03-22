## Design

### System overview
<!-- TODO: I think this should be in another section, but I'll just write it now and move it to the right place later on-->
This project is split up in two main parts called the frontend and backend.
There are a couple of reasons for doing this:
- Separation between the business logic and it's presented to the user. All the work gets done in the backend while the frontend only displays the data delivered by the backend. This nicely separates the logic from the UI which just makes the code more clean and easier to understand. UI creation code isn't mixed with the logic which allows for easier changes on both parts
- This project interacts with a few APIs that require authentication. If I were to fetch these APIs from the same programs as the one that displays it, it would be quite simple to just take a snapshot of the memory and steal the API credentials and use them for criminal gain. This would obviously result in getting a huge bill by Google Maps because some criminal sent requests in my name using my API key. Moving the whole fetching and calculation process to the backend (that's running on my own server) makes it impossible for criminals to just steal the API key from the application unless my server has a vulnerability.
- Having a backend that's just an API delivering data makes it easy to setup an alternative frontend. This is especially helpful if your original fronted doesn't turn out to be how you want it. You can start developing another frontend while keeping the old frontend available for users that prefer it. Reddit has done this and still keeps its old (and still quite popular) frontend at https://old.reddit.com while the new frontend is available at https://reddit.com
<!--TODO: Explain something with the SPA -->
- In case you have/gain a lot of users that want to use you system at the same time, you can scale everything way better, have different servers that deliver the static files required by the frontend (the HTML, CSS and JS files) and some other backend servers that deliver the content. This scales way better than if you just have a backend that generates the frontend code
### Frontend

### Backend