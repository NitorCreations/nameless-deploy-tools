# NDT Command Reference

## `ndt account-id`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt add-deployer-server`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt assume-role`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt assumed-role-name`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt bake-docker`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt bake-image`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt cf-delete-stack`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt cf-follow-logs`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt cf-get-parameter`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt cf-logical-id`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt cf-region`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt cf-signal-status`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt cf-stack-id`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt cf-stack-name`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt create-account`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt create-stack`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt deploy-cdk`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt deploy-serverless`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt deploy-stack`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt deploy-terraform`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt detach-volume`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt ec2-clean-snapshots`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt ec2-get-tag`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt ec2-get-userdata`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt ec2-instance-id`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt ec2-region`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt ec2-wait-for-metadata`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt ecr-ensure-repo`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt ecr-repo-uri`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt enable-profile`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt get-images`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt interpolate-file`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt json-to-yaml`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt latest-snapshot`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt list-components`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt list-file-to-json`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt list-jobs`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt load-parameters`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt logs`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt mfa-add-token`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt mfa-backup`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt mfa-code`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt mfa-delete-token`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt mfa-qrcode`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt print-create-instructions`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt profile-expiry-to-env`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt profile-to-env`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt promote-image`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt pytail`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt read-profile-expiry`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt region`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt register-private-dns`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt session-to-env`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt setup-cli`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt share-to-another-region`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt show-stack-params-and-outputs`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt show-terraform-params`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt snapshot-from-volume`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt terraform-pull-state`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt undeploy-cdk`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt undeploy-serverless`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt undeploy-stack`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt undeploy-terraform`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt upsert-cloudfront-records`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt volume-from-snapshot`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt yaml-to-json`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `ndt yaml-to-yaml`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ndt", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `[ndt ]associate-eip`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/associate-eip", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `[ndt ]cf-logs-to-cloudwatch`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/cf-logs-to-cloudwatch", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `[ndt ]ec2-associate-eip`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/ec2-associate-eip", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `[ndt ]logs-to-cloudwatch`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/logs-to-cloudwatch", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `[ndt ]n-include`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/n-include", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `[ndt ]n-include-all`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/n-include-all", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `[ndt ]signal-cf-status`

```bash
Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 578, in _build_master
    ws.require(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 895, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 786, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (ec2-utils 0.18 (/home/pasi/src/ec2-utils), Requirement.parse(\'ec2-utils==0.17\'), {\'nameless-deploy-tools\'})

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pasi/.pyenv/versions/3.7.2/bin/signal-cf-status", line 6, in <module>
    from pkg_resources import load_entry_point
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3112, in <module>
    @_call_aside
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3096, in _call_aside
    f(*args, **kwargs)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3125, in _initialize_master_working_set
    working_set = WorkingSet._build_master()
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 580, in _build_master
    return cls._build_from_requirements(__requires__)
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 593, in _build_from_requirements
    dists = ws.resolve(reqs, Environment())
  File "/home/pasi/.pyenv/versions/3.7.2/lib/python3.7/site-packages/pkg_resources/__init__.py", line 781, in resolve
    raise DistributionNotFound(req, requirers)
pkg_resources.DistributionNotFound: The \'ec2-utils==0.17\' distribution was not found and is required by nameless-deploy-tools
```

## `create-shell-archive.sh`

```bash
file  one or more files to package into the archive
usage: create-shell-archive.sh [-h] [<file> ...]

Creates a self-extracting bash archive, suitable for storing in e.g. Lastpass SecureNotes
positional arguments:

optional arguments:
  -h, --help  show this help message and exit
```

## `encrypt-and-mount.sh`

```bash
Mounts a local block device as an encrypted volume. Handy for things like local database installs.
usage: encrypt-and-mount.sh [-h] blk-device mount-path


positional arguments
  blk-device  the block device you want to encrypt and mount
  mount-path  the mount point for the encrypted volume

optional arguments:
  -h, --help  show this help message and exit
```

## `ensure-letsencrypt-certs.sh`

```bash
usage: ensure-letsencrypt-certs.sh [-h] domain-name [domain-name ...]

Fetches a certificate with fetch-secrets.sh, and exits cleanly if certificate is found and valid.
Otherwise gets a new certificate from letsencrypt via DNS verification using Route53.
Requires that fetch-secrets.sh and Route53 are set up correctly.

positional arguments
  domain-name   The domain(s) you want to check certificates for

optional arguments:
  -h, --help  show this help message and exit
```

## `lastpass-fetch-notes.sh`

```bash
--optional  marks that following files will not fail and exit the script in they do not exist
usage: lasptass-fetch-notes.sh [-h] mode file [file ...] [--optional file ...]

Fetches secure notes from lastpass that match the basename of each listed file.
Files specified after --optional won\'t fail if the file does not exist.

positional arguments
  mode   the file mode for the downloaded files
  file   the file(s) to download. The source will be the note that matches the basename of the file

optional arguments:
  -h, --help  show this help message and exit
```

## `lpssh`

```bash
usage: lpssh [-h] [-k key-name] user@example.com

Fetches key mappings from lastpass, downloads mapped keys into a local ssh-agent and starts
an ssh session using those credentials.

positional arguments
  user@example.com   The user and host to match in "my-ssh-mappings" secure note
                     and to log into once keys are set up.

optional arguments:
  -k,         key name in lastpass to use if you don\'t want to use a mapping
  -h, --help  show this help message and exit
```

## `mount-and-format.sh`

```bash
Mounts a local block device as an encrypted volume. Handy for things like local database installs.
usage: mount-and-format.sh [-h] blk-device mount-path


positional arguments
  blk-device  the block device you want to mount and formant
  mount-path  the mount point for the volume

optional arguments:
  -h, --help  show this help message and exit
```

## `setup-fetch-secrets.sh`

```bash
Please run as root
usage: setup-fetch-secrets.sh [-h] <lpass|s3|vault>

Sets up a global fetch-secrets.sh that fetches secrets from either LastPass, S3 or nitor-vault

positional arguments
  lpass|s3|vault   the selected secrets backend.

optional arguments:
  -h, --help  show this help message and exit exit 1
```

## `ssh-hostkeys-collect.sh`

```bash
usage: ssh-hostkeys-collect.sh [-h] hostname

Creates a <hostname>-ssh-hostkeys.sh archive in the current directory containing
ssh host keys to preserve the identity of a server over image upgrades.

positional arguments
  hostname   the name of the host used to store the keys. Typically the hostname is what
             instance userdata scripts will use to look for the keys

optional arguments:
  -h, --help  show this help message and exit
```

