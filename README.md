# ReverendTranslated

This is a site hosted utilizing flask, it takes pages of RI's chapters from other sites and translate them by using google translate via selenium

The objective to be reached is spreading Gu Zhen Ren's work across the globe by making sure everyone can read it

The translation is not perfect of course, but it is for sure better than those MTL sites; the version of RI that is translated is in english, instead of the original chinese version, this might cause a further loss in meaning, thats why i'll be trying to add an option to choose which version to choose

As of now the project is still not really made to be used:
1. the site lacks a good UI
2. the requests arent handled in parallel due to selenium's limitations, this means that the entire way the project work will have to be revolutionized
3. there might be a bunch of issues with the translation, since the project is made for everyone it is right that those who find errors in the translation and want to fix the issue must be able to do so

TODO:
make the server load the next chapter the person is reading
make a main page
store cookies to make users not select dark/light mode every time
make a page for chapter 0 and 2335
