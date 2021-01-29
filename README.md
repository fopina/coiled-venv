# coil
Let it [hatch](https://github.com/ofek/hatch), watch it [coil](https://www.google.com/search?q=coiled+python&tbm=isch)

[hatch](https://github.com/ofek/hatch) is a great virtualenv manager IMHO. But pure virtualenv management can be simpler!

*coil* aims to be as simple as possible and with no external dependencies: keep the OS site-packages clean, that's why we use virtualenvs to start!

## the future

```
➜ myproject coil
No env configured for /home/fopina/projects/myproject
➜ myproject coil -c thisenv
/home/fopina/.virtualenvs/thisenv created
/home/fopina/.virtualenvs/thisenv assigned to /home/fopina/projects/myproject
/home/fopina/.virtualenvs/thisenv loaded
(thisenv) ➜  myproject 
```

Once an env is created and assigned to a path it can be loaded without any hassle

```
➜ myproject coil
/home/fopina/.virtualenvs/thisenv assigned to /home/fopina/projects/myproject
/home/fopina/.virtualenvs/thisenv loaded
(thisenv) ➜  myproject 
```

Same env is loaded from any subdirectory

```
➜ src pwd
/home/fopina/projects/myproject/src
➜ src coil
/home/fopina/.virtualenvs/thisenv assigned to /home/fopina/projects/myproject
/home/fopina/.virtualenvs/thisenv loaded
(thisenv) ➜  src 
```

And it can assigned/re-used by as many paths as you want

```
➜ otherproject coil
No env configured for /home/fopina/projects/otherproject
➜ myproject coil thisenv
/home/fopina/.virtualenvs/thisenv assigned to /home/fopina/projects/otherproject
/home/fopina/.virtualenvs/thisenv loaded
(thisenv) ➜  otherproject 
```
