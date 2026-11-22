---
title: Command Line Interface | Guide
outline: deep
---

<a id="command-line-interface"></a>
# Command Line Interface

<a id="commands"></a>
## Commands

<a id="vitest"></a>
### `vitest`

Start Vitest in the current directory. Will enter the watch mode in development environment and run mode in CI (or non-interactive terminal) automatically.

You can pass an additional argument as the filter of the test files to run. For example:

```bash
vitest foobar
```

Will run only the test file that contains `foobar` in their paths. This filter only checks inclusion and doesn't support regexp or glob patterns (unless your terminal processes it before Vitest receives the filter).

Since Vitest 3, you can also specify the test by filename and line number:

```bash
$ vitest basic/foo.test.ts:10
```

**Warning**
Note that Vitest requires the full filename for this feature to work. It can be relative to the current working directory or an absolute file path.

```bash
$ vitest basic/foo.js:10 # ✅
$ vitest ./basic/foo.js:10 # ✅
$ vitest /users/project/basic/foo.js:10 # ✅
$ vitest foo:10 # ❌
$ vitest ./basic/foo:10 # ❌
```

At the moment Vitest also doesn't support ranges:

```bash
$ vitest basic/foo.test.ts:10, basic/foo.test.ts:25 # ✅
$ vitest basic/foo.test.ts:10-25 # ❌
```

<a id="vitest-run"></a>
### `vitest run`

Perform a single run without watch mode.

<a id="vitest-watch"></a>
### `vitest watch`

Run all test suites but watch for changes and rerun tests when they change. Same as calling `vitest` without an argument. Will fallback to `vitest run` in CI or when stdin is not a TTY (non-interactive environment).

<a id="vitest-dev"></a>
### `vitest dev`

Alias to `vitest watch`.

<a id="vitest-related"></a>
### `vitest related`

Run only tests that cover a list of source files. Works with static imports (e.g., `import('./index.js')` or `import index from './index.js`), but not the dynamic ones (e.g., `import(filepath)`). All files should be relative to root folder.

Useful to run with [`lint-staged`](https://github.com/okonet/lint-staged) or with your CI setup.

```bash
vitest related /src/index.ts /src/hello-world.js
```

**Tip**
Don't forget that Vitest runs with enabled watch mode by default. If you are using tools like `lint-staged`, you  should also pass `--run` option, so that command can exit normally.

```js [.lintstagedrc.js]
export default {
  '*.{js,ts}': 'vitest related --run',
}
```

<a id="vitest-bench"></a>
### `vitest bench`

Run only [benchmark](https://vitest.dev/guide/features.html#benchmarking) tests, which compare performance results.

<a id="vitest-init"></a>
### `vitest init`

`vitest init <name>` can be used to setup project configuration. At the moment, it only supports [`browser`](browser/index.md) value:

```bash
vitest init browser
```

<a id="vitest-list"></a>
### `vitest list`

`vitest list` command inherits all `vitest` options to print the list of all matching tests. This command ignores `reporters` option. By default, it will print the names of all tests that matched the file filter and name pattern:

```shell
vitest list filename.spec.ts -t="some-test"
```

```txt
describe > some-test
describe > some-test > test 1
describe > some-test > test 2
```

You can pass down `--json` flag to print tests in JSON format or save it in a separate file:

```bash
vitest list filename.spec.ts -t="some-test" --json=./file.json
```

If `--json` flag doesn't receive a value, it will output the JSON into stdout.

You also can pass down `--filesOnly` flag to print the test files only:

```bash
vitest list --filesOnly
```

```txt
tests/test1.test.ts
tests/test2.test.ts
```

Since Vitest 4.1, you may pass `--static-parse` to [parse test files](https://vitest.dev/api/advanced/vitest#parsespecifications) instead of running them to collect tests. Vitest parses test files with limited concurrency, defaulting to `os.availableParallelism()`. You can change it via the `--static-parse-concurrency` option.

<a id="shell-autocompletions"></a>
## Shell Autocompletions

Vitest provides shell autocompletions for commands, options, and option values powered by [`@bomb.sh/tab`](https://github.com/bombshell-dev/tab).

<a id="setup"></a>
### Setup

For permanent setup in zsh, add this to your `~/.zshrc`:

```bash
# Add to ~/.zshrc for permanent autocompletions (same can be done for other shells)
source <(vitest complete zsh)
```

<a id="package-manager-integration"></a>
### Package Manager Integration

`@bomb.sh/tab` integrates with [package managers](https://github.com/bombshell-dev/tab?tab=readme-ov-file#package-manager-completions). Autocompletions work when running vitest directly:


```bash [npm]
npm vitest <Tab>
```

```bash [npm]
npm exec vitest <Tab>
```

```bash [pnpm]
pnpm vitest <Tab>
```

```bash [yarn]
yarn vitest <Tab>
```

```bash [bun]
bun vitest <Tab>
```


For package manager autocompletions, you should install [tab's package manager completions](https://github.com/bombshell-dev/tab?tab=readme-ov-file#package-manager-completions) separately.

<a id="options"></a>
## Options

**Tip**
Vitest supports both camel case and kebab case for [CLI arguments](https://github.com/cacjs/cac#dot-nested-options). For example, `--passWithNoTests` and `--pass-with-no-tests` will both work (`--no-color` and `--inspect-brk` are the exceptions).

Vitest also supports different ways of specifying the value: `--reporter dot` and `--reporter=dot` are both valid.

If option supports an array of values, you need to pass the option multiple times:

```
vitest --reporter=dot --reporter=default
```

Boolean options can be negated with `no-` prefix. Specifying the value as `false` also works:

```
vitest --no-api
vitest --api=false
```

<a id="root"></a>
### root

- **CLI:** `-r, --root <path>`
- **Config:** [root](https://vitest.dev/config/root)

Root path

<a id="config"></a>
### config

- **CLI:** `-c, --config <path>`

Path to config file

<a id="update"></a>
### update

- **CLI:** `-u, --update [type]`
- **Config:** [update](https://vitest.dev/config/update)

Update snapshot (accepts boolean, "new", "all" or "none")

<a id="watch"></a>
### watch

- **CLI:** `-w, --watch`
- **Config:** [watch](https://vitest.dev/config/watch)

Enable watch mode

<a id="testnamepattern"></a>
### testNamePattern

- **CLI:** `-t, --testNamePattern <pattern>`
- **Config:** [testNamePattern](https://vitest.dev/config/testnamepattern)

Run tests with full names matching the specified regexp pattern

<a id="dir"></a>
### dir

- **CLI:** `--dir <path>`
- **Config:** [dir](https://vitest.dev/config/dir)

Base directory to scan for the test files

<a id="ui"></a>
### ui

- **CLI:** `--ui`

Enable UI

<a id="open"></a>
### open

- **CLI:** `--open`
- **Config:** [open](https://vitest.dev/config/open)

Open UI automatically (default: `!process.env.CI`)

<a id="api-port"></a>
### api.port

- **CLI:** `--api.port [port]`

Specify server port. Note if the port is already being used, Vite will automatically try the next available port so this may not be the actual port the server ends up listening on. If true will be set to `51204`

<a id="api-host"></a>
### api.host

- **CLI:** `--api.host [host]`

Specify which IP addresses the server should listen on. Set this to `0.0.0.0` or `true` to listen on all addresses, including LAN and public addresses

<a id="api-strictport"></a>
### api.strictPort

- **CLI:** `--api.strictPort`

Set to true to exit if port is already in use, instead of automatically trying the next available port

<a id="api-allowexec"></a>
### api.allowExec

- **CLI:** `--api.allowExec`
- **Config:** [api.allowExec](https://vitest.dev/config/api#api-allowexec)

Allow API to execute code. (Be careful when enabling this option in untrusted environments)

<a id="api-allowwrite"></a>
### api.allowWrite

- **CLI:** `--api.allowWrite`
- **Config:** [api.allowWrite](https://vitest.dev/config/api#api-allowwrite)

Allow API to edit files. (Be careful when enabling this option in untrusted environments)

<a id="silent"></a>
### silent

- **CLI:** `--silent [value]`
- **Config:** [silent](https://vitest.dev/config/silent)

Silent console output from tests. Use `'passed-only'` to see logs from failing tests only.

<a id="hideskippedtests"></a>
### hideSkippedTests

- **CLI:** `--hideSkippedTests`

Hide logs for skipped tests

<a id="reporters"></a>
### reporters

- **CLI:** `--reporter <name>`
- **Config:** [reporters](https://vitest.dev/config/reporters)

Specify reporters (default, agent, minimal, blob, verbose, dot, json, tap, tap-flat, junit, tree, hanging-process, github-actions)

<a id="outputfile"></a>
### outputFile

- **CLI:** `--outputFile <filename/-s>`
- **Config:** [outputFile](https://vitest.dev/config/outputfile)

Write test results to a file when supporter reporter is also specified, use cac's dot notation for individual outputs of multiple reporters (example: `--outputFile.tap=./tap.txt`)

<a id="coverage-provider"></a>
### coverage.provider

- **CLI:** `--coverage.provider <name>`
- **Config:** [coverage.provider](https://vitest.dev/config/coverage#coverage-provider)

Select the tool for coverage collection, available values are: "v8", "istanbul" and "custom"

<a id="coverage-enabled"></a>
### coverage.enabled

- **CLI:** `--coverage.enabled`
- **Config:** [coverage.enabled](https://vitest.dev/config/coverage#coverage-enabled)

Enables coverage collection. Can be overridden using the `--coverage` CLI option (default: `false`)

<a id="coverage-include"></a>
### coverage.include

- **CLI:** `--coverage.include <pattern>`
- **Config:** [coverage.include](https://vitest.dev/config/coverage#coverage-include)

Files included in coverage as glob patterns. May be specified more than once when using multiple patterns. By default only files covered by tests are included.

<a id="coverage-exclude"></a>
### coverage.exclude

- **CLI:** `--coverage.exclude <pattern>`
- **Config:** [coverage.exclude](https://vitest.dev/config/coverage#coverage-exclude)

Files to be excluded in coverage. May be specified more than once when using multiple extensions.

<a id="coverage-clean"></a>
### coverage.clean

- **CLI:** `--coverage.clean`
- **Config:** [coverage.clean](https://vitest.dev/config/coverage#coverage-clean)

Clean coverage results before running tests (default: true)

<a id="coverage-cleanonrerun"></a>
### coverage.cleanOnRerun

- **CLI:** `--coverage.cleanOnRerun`
- **Config:** [coverage.cleanOnRerun](https://vitest.dev/config/coverage#coverage-cleanonrerun)

Clean coverage report on watch rerun (default: true)

<a id="coverage-reportsdirectory"></a>
### coverage.reportsDirectory

- **CLI:** `--coverage.reportsDirectory <path>`
- **Config:** [coverage.reportsDirectory](https://vitest.dev/config/coverage#coverage-reportsdirectory)

Directory to write coverage report to (default: ./coverage)

<a id="coverage-reporter"></a>
### coverage.reporter

- **CLI:** `--coverage.reporter <name>`
- **Config:** [coverage.reporter](https://vitest.dev/config/coverage#coverage-reporter)

Coverage reporters to use. Visit [`coverage.reporter`](https://vitest.dev/config/coverage#coverage-reporter) for more information (default: `["text", "html", "clover", "json"]`)

<a id="coverage-reportonfailure"></a>
### coverage.reportOnFailure

- **CLI:** `--coverage.reportOnFailure`
- **Config:** [coverage.reportOnFailure](https://vitest.dev/config/coverage#coverage-reportonfailure)

Generate coverage report even when tests fail (default: `false`)

<a id="coverage-allowexternal"></a>
### coverage.allowExternal

- **CLI:** `--coverage.allowExternal`
- **Config:** [coverage.allowExternal](https://vitest.dev/config/coverage#coverage-allowexternal)

Collect coverage of files outside the project root (default: `false`)

<a id="coverage-skipfull"></a>
### coverage.skipFull

- **CLI:** `--coverage.skipFull`
- **Config:** [coverage.skipFull](https://vitest.dev/config/coverage#coverage-skipfull)

Do not show files with 100% statement, branch, and function coverage (default: `false`)

<a id="coverage-thresholds-100"></a>
### coverage.thresholds.100

- **CLI:** `--coverage.thresholds.100`
- **Config:** [coverage.thresholds.100](https://vitest.dev/config/coverage#coverage-thresholds-100)

Shortcut to set all coverage thresholds to 100 (default: `false`)

<a id="coverage-thresholds-perfile"></a>
### coverage.thresholds.perFile

- **CLI:** `--coverage.thresholds.perFile`
- **Config:** [coverage.thresholds.perFile](https://vitest.dev/config/coverage#coverage-thresholds-perfile)

Check thresholds per file. See `--coverage.thresholds.lines`, `--coverage.thresholds.functions`, `--coverage.thresholds.branches` and `--coverage.thresholds.statements` for the actual thresholds (default: `false`)

<a id="coverage-thresholds-autoupdate"></a>
### coverage.thresholds.autoUpdate

- **CLI:** `--coverage.thresholds.autoUpdate <boolean|function>`
- **Config:** [coverage.thresholds.autoUpdate](https://vitest.dev/config/coverage#coverage-thresholds-autoupdate)

Update threshold values: "lines", "functions", "branches" and "statements" to configuration file when current coverage is above the configured thresholds (default: `false`)

<a id="coverage-thresholds-lines"></a>
### coverage.thresholds.lines

- **CLI:** `--coverage.thresholds.lines <number>`

Threshold for lines. Visit [istanbuljs](https://github.com/istanbuljs/nyc#coverage-thresholds) for more information. This option is not available for custom providers

<a id="coverage-thresholds-functions"></a>
### coverage.thresholds.functions

- **CLI:** `--coverage.thresholds.functions <number>`

Threshold for functions. Visit [istanbuljs](https://github.com/istanbuljs/nyc#coverage-thresholds) for more information. This option is not available for custom providers

<a id="coverage-thresholds-branches"></a>
### coverage.thresholds.branches

- **CLI:** `--coverage.thresholds.branches <number>`

Threshold for branches. Visit [istanbuljs](https://github.com/istanbuljs/nyc#coverage-thresholds) for more information. This option is not available for custom providers

<a id="coverage-thresholds-statements"></a>
### coverage.thresholds.statements

- **CLI:** `--coverage.thresholds.statements <number>`

Threshold for statements. Visit [istanbuljs](https://github.com/istanbuljs/nyc#coverage-thresholds) for more information. This option is not available for custom providers

<a id="coverage-ignoreclassmethods"></a>
### coverage.ignoreClassMethods

- **CLI:** `--coverage.ignoreClassMethods <name>`
- **Config:** [coverage.ignoreClassMethods](https://vitest.dev/config/coverage#coverage-ignoreclassmethods)

Array of class method names to ignore for coverage. Visit [istanbuljs](https://github.com/istanbuljs/nyc#ignoring-methods) for more information. This option is only available for the istanbul providers (default: `[]`)

<a id="coverage-processingconcurrency"></a>
### coverage.processingConcurrency

- **CLI:** `--coverage.processingConcurrency <number>`
- **Config:** [coverage.processingConcurrency](https://vitest.dev/config/coverage#coverage-processingconcurrency)

Concurrency limit used when processing the coverage results. (default min between 20 and the number of CPUs)

<a id="coverage-customprovidermodule"></a>
### coverage.customProviderModule

- **CLI:** `--coverage.customProviderModule <path>`
- **Config:** [coverage.customProviderModule](https://vitest.dev/config/coverage#coverage-customprovidermodule)

Specifies the module name or path for the custom coverage provider module. Visit [Custom Coverage Provider](coverage.md#custom-coverage-provider) for more information. This option is only available for custom providers

<a id="coverage-watermarks-statements"></a>
### coverage.watermarks.statements

- **CLI:** `--coverage.watermarks.statements <watermarks>`

High and low watermarks for statements in the format of `<high>,<low>`

<a id="coverage-watermarks-lines"></a>
### coverage.watermarks.lines

- **CLI:** `--coverage.watermarks.lines <watermarks>`

High and low watermarks for lines in the format of `<high>,<low>`

<a id="coverage-watermarks-branches"></a>
### coverage.watermarks.branches

- **CLI:** `--coverage.watermarks.branches <watermarks>`

High and low watermarks for branches in the format of `<high>,<low>`

<a id="coverage-watermarks-functions"></a>
### coverage.watermarks.functions

- **CLI:** `--coverage.watermarks.functions <watermarks>`

High and low watermarks for functions in the format of `<high>,<low>`

<a id="coverage-changed"></a>
### coverage.changed

- **CLI:** `--coverage.changed <commit/branch>`
- **Config:** [coverage.changed](https://vitest.dev/config/coverage#coverage-changed)

Collect coverage only for files changed since a specified commit or branch (e.g., `origin/main` or `HEAD~1`). Inherits value from `--changed` by default.

<a id="coverage-excludeafterremap"></a>
### coverage.excludeAfterRemap

- **CLI:** `--coverage.excludeAfterRemap`
- **Config:** [coverage.excludeAfterRemap](https://vitest.dev/config/coverage#coverage-excludeafterremap)

Apply exclusions again after coverage has been remapped to original sources. (default: false)

<a id="coverage-htmldir"></a>
### coverage.htmlDir

- **CLI:** `--coverage.htmlDir <path>`
- **Config:** [coverage.htmlDir](https://vitest.dev/config/coverage#coverage-htmldir)

Directory of HTML coverage output to be served in UI mode and HTML reporter.

<a id="mode"></a>
### mode

- **CLI:** `--mode <name>`
- **Config:** [mode](https://vitest.dev/config/mode)

Override Vite mode (default: `test` or `benchmark`)

<a id="isolate"></a>
### isolate

- **CLI:** `--isolate`
- **Config:** [isolate](https://vitest.dev/config/isolate)

Run every test file in isolation. To disable isolation, use `--no-isolate` (default: `true`)

<a id="globals"></a>
### globals

- **CLI:** `--globals`
- **Config:** [globals](https://vitest.dev/config/globals)

Inject apis globally

<a id="dom"></a>
### dom

- **CLI:** `--dom`

Mock browser API with happy-dom

<a id="browser-enabled"></a>
### browser.enabled

- **CLI:** `--browser.enabled`
- **Config:** [browser.enabled](https://vitest.dev/config/browser/enabled)

Run tests in the browser. Equivalent to `--browser.enabled` (default: `false`)

<a id="browser-name"></a>
### browser.name

- **CLI:** `--browser.name <name>`

Run all tests in a specific browser. Some browsers are only available for specific providers (see `--browser.provider`).

<a id="browser-headless"></a>
### browser.headless

- **CLI:** `--browser.headless`
- **Config:** [browser.headless](https://vitest.dev/config/browser/headless)

Run the browser in headless mode (i.e. without opening the GUI (Graphical User Interface)). If you are running Vitest in CI, it will be enabled by default (default: `process.env.CI`)

<a id="browser-api-port"></a>
### browser.api.port

- **CLI:** `--browser.api.port [port]`
- **Config:** [browser.api.port](https://vitest.dev/config/browser/api#api-port)

Specify server port. Note if the port is already being used, Vite will automatically try the next available port so this may not be the actual port the server ends up listening on. If true will be set to `63315`

<a id="browser-api-host"></a>
### browser.api.host

- **CLI:** `--browser.api.host [host]`
- **Config:** [browser.api.host](https://vitest.dev/config/browser/api#api-host)

Specify which IP addresses the server should listen on. Set this to `0.0.0.0` or `true` to listen on all addresses, including LAN and public addresses

<a id="browser-api-strictport"></a>
### browser.api.strictPort

- **CLI:** `--browser.api.strictPort`
- **Config:** [browser.api.strictPort](https://vitest.dev/config/browser/api#api-strictport)

Set to true to exit if port is already in use, instead of automatically trying the next available port

<a id="browser-api-allowexec"></a>
### browser.api.allowExec

- **CLI:** `--browser.api.allowExec`
- **Config:** [browser.api.allowExec](https://vitest.dev/config/browser/api#api-allowexec)

Allow API to execute code. (Be careful when enabling this option in untrusted environments)

<a id="browser-api-allowwrite"></a>
### browser.api.allowWrite

- **CLI:** `--browser.api.allowWrite`
- **Config:** [browser.api.allowWrite](https://vitest.dev/config/browser/api#api-allowwrite)

Allow API to edit files. (Be careful when enabling this option in untrusted environments)

<a id="browser-isolate"></a>
### browser.isolate

- **CLI:** `--browser.isolate`
- **Config:** [browser.isolate](https://vitest.dev/config/browser/isolate)

Run every browser test file in isolation. To disable isolation, use `--browser.isolate=false` (default: `true`)

<a id="browser-ui"></a>
### browser.ui

- **CLI:** `--browser.ui`
- **Config:** [browser.ui](https://vitest.dev/config/browser/ui)

Show Vitest UI when running tests (default: `!process.env.CI`)

<a id="browser-detailspanelposition"></a>
### browser.detailsPanelPosition

- **CLI:** `--browser.detailsPanelPosition <position>`
- **Config:** [browser.detailsPanelPosition](https://vitest.dev/config/browser/detailspanelposition)

Default position for the details panel in browser mode. Either `right` (horizontal split) or `bottom` (vertical split) (default: `right`)

<a id="browser-fileparallelism"></a>
### browser.fileParallelism

- **CLI:** `--browser.fileParallelism`

Should browser test files run in parallel. Use `--browser.fileParallelism=false` to disable (default: `true`)

<a id="browser-connecttimeout"></a>
### browser.connectTimeout

- **CLI:** `--browser.connectTimeout <timeout>`
- **Config:** [browser.connectTimeout](https://vitest.dev/config/browser/connecttimeout)

If connection to the browser takes longer, the test suite will fail (default: `60_000`)

<a id="browser-trackunhandlederrors"></a>
### browser.trackUnhandledErrors

- **CLI:** `--browser.trackUnhandledErrors`
- **Config:** [browser.trackUnhandledErrors](https://vitest.dev/config/browser/trackunhandlederrors)

Control if Vitest catches uncaught exceptions so they can be reported (default: `true`)

<a id="browser-trace"></a>
### browser.trace

- **CLI:** `--browser.trace <mode>`
- **Config:** [browser.trace](https://vitest.dev/config/browser/trace)

Enable trace view mode. Supported: "on", "off", "on-first-retry", "on-all-retries", "retain-on-failure".

<a id="browser-locators-exact"></a>
### browser.locators.exact

- **CLI:** `--browser.locators.exact`
- **Config:** [browser.locators.exact](https://vitest.dev/config/browser/locators#locators-exact)

Should locators match the text exactly by default (default: `false`)

<a id="pool"></a>
### pool

- **CLI:** `--pool <pool>`
- **Config:** [pool](https://vitest.dev/config/pool)

Specify pool, if not running in the browser (default: `forks`)

<a id="execargv"></a>
### execArgv

- **CLI:** `--execArgv <option>`
- **Config:** [execArgv](https://vitest.dev/config/execargv)

Pass additional arguments to `node` process when spawning `worker_threads` or `child_process`.

<a id="vmmemorylimit"></a>
### vmMemoryLimit

- **CLI:** `--vmMemoryLimit <limit>`
- **Config:** [vmMemoryLimit](https://vitest.dev/config/vmmemorylimit)

Memory limit for VM pools. If you see memory leaks, try to tinker this value.

<a id="fileparallelism"></a>
### fileParallelism

- **CLI:** `--fileParallelism`
- **Config:** [fileParallelism](https://vitest.dev/config/fileparallelism)

Should all test files run in parallel. Use `--no-file-parallelism` to disable (default: `true`)

<a id="maxworkers"></a>
### maxWorkers

- **CLI:** `--maxWorkers <workers>`
- **Config:** [maxWorkers](https://vitest.dev/config/maxworkers)

Maximum number or percentage of workers to run tests in

<a id="environment"></a>
### environment

- **CLI:** `--environment <name>`
- **Config:** [environment](https://vitest.dev/config/environment)

Specify runner environment, if not running in the browser (default: `node`)

<a id="passwithnotests"></a>
### passWithNoTests

- **CLI:** `--passWithNoTests`
- **Config:** [passWithNoTests](https://vitest.dev/config/passwithnotests)

Pass when no tests are found

<a id="logheapusage"></a>
### logHeapUsage

- **CLI:** `--logHeapUsage`
- **Config:** [logHeapUsage](https://vitest.dev/config/logheapusage)

Show the size of heap for each test when running in node

<a id="detectasyncleaks"></a>
### detectAsyncLeaks

- **CLI:** `--detectAsyncLeaks`
- **Config:** [detectAsyncLeaks](https://vitest.dev/config/detectasyncleaks)

Detect asynchronous resources leaking from the test file (default: `false`)

<a id="allowonly"></a>
### allowOnly

- **CLI:** `--allowOnly`
- **Config:** [allowOnly](https://vitest.dev/config/allowonly)

Allow tests and suites that are marked as only (default: `!process.env.CI`)

<a id="dangerouslyignoreunhandlederrors"></a>
### dangerouslyIgnoreUnhandledErrors

- **CLI:** `--dangerouslyIgnoreUnhandledErrors`
- **Config:** [dangerouslyIgnoreUnhandledErrors](https://vitest.dev/config/dangerouslyignoreunhandlederrors)

Ignore any unhandled errors that occur

<a id="sequence-shuffle-files"></a>
### sequence.shuffle.files

- **CLI:** `--sequence.shuffle.files`
- **Config:** [sequence.shuffle.files](https://vitest.dev/config/sequence#sequence-shuffle-files)

Run files in a random order. Long running tests will not start earlier if you enable this option. (default: `false`)

<a id="sequence-shuffle-tests"></a>
### sequence.shuffle.tests

- **CLI:** `--sequence.shuffle.tests`
- **Config:** [sequence.shuffle.tests](https://vitest.dev/config/sequence#sequence-shuffle-tests)

Run tests in a random order (default: `false`)

<a id="sequence-concurrent"></a>
### sequence.concurrent

- **CLI:** `--sequence.concurrent`
- **Config:** [sequence.concurrent](https://vitest.dev/config/sequence#sequence-concurrent)

Make tests run in parallel (default: `false`)

<a id="sequence-seed"></a>
### sequence.seed

- **CLI:** `--sequence.seed <seed>`
- **Config:** [sequence.seed](https://vitest.dev/config/sequence#sequence-seed)

Set the randomization seed. This option will have no effect if `--sequence.shuffle` is falsy. Visit ["Random Seed" page](https://en.wikipedia.org/wiki/Random_seed) for more information

<a id="sequence-hooks"></a>
### sequence.hooks

- **CLI:** `--sequence.hooks <order>`
- **Config:** [sequence.hooks](https://vitest.dev/config/sequence#sequence-hooks)

Changes the order in which hooks are executed. Accepted values are: "stack", "list" and "parallel". Visit [`sequence.hooks`](https://vitest.dev/config/sequence#sequence-hooks) for more information (default: `"parallel"`)

<a id="sequence-setupfiles"></a>
### sequence.setupFiles

- **CLI:** `--sequence.setupFiles <order>`
- **Config:** [sequence.setupFiles](https://vitest.dev/config/sequence#sequence-setupfiles)

Changes the order in which setup files are executed. Accepted values are: "list" and "parallel". If set to "list", will run setup files in the order they are defined. If set to "parallel", will run setup files in parallel (default: `"parallel"`)

<a id="inspect"></a>
### inspect

- **CLI:** `--inspect [[host:]port]`

Enable Node.js inspector (default: `127.0.0.1:9229`)

<a id="inspectbrk"></a>
### inspectBrk

- **CLI:** `--inspectBrk [[host:]port]`

Enable Node.js inspector and break before the test starts

<a id="testtimeout"></a>
### testTimeout

- **CLI:** `--testTimeout <timeout>`
- **Config:** [testTimeout](https://vitest.dev/config/testtimeout)

Default timeout of a test in milliseconds (default: `5000`). Use `0` to disable timeout completely.

<a id="hooktimeout"></a>
### hookTimeout

- **CLI:** `--hookTimeout <timeout>`
- **Config:** [hookTimeout](https://vitest.dev/config/hooktimeout)

Default hook timeout in milliseconds (default: `10000`). Use `0` to disable timeout completely.

<a id="bail"></a>
### bail

- **CLI:** `--bail <number>`
- **Config:** [bail](https://vitest.dev/config/bail)

Stop test execution when given number of tests have failed (default: `0`)

<a id="retry-count"></a>
### retry.count

- **CLI:** `--retry.count <times>`
- **Config:** [retry.count](https://vitest.dev/config/retry#retry-count)

Number of times to retry a test if it fails (default: `0`)

<a id="retry-delay"></a>
### retry.delay

- **CLI:** `--retry.delay <ms>`
- **Config:** [retry.delay](https://vitest.dev/config/retry#retry-delay)

Delay in milliseconds between retry attempts (default: `0`)

<a id="retry-condition"></a>
### retry.condition

- **CLI:** `--retry.condition <pattern>`
- **Config:** [retry.condition](https://vitest.dev/config/retry#retry-condition)

Regex pattern to match error messages that should trigger a retry. Only errors matching this pattern will cause a retry (default: retry on all errors)

<a id="diff-aannotation"></a>
### diff.aAnnotation

- **CLI:** `--diff.aAnnotation <annotation>`
- **Config:** [diff.aAnnotation](https://vitest.dev/config/diff#diff-aannotation)

Annotation for expected lines (default: `Expected`)

<a id="diff-aindicator"></a>
### diff.aIndicator

- **CLI:** `--diff.aIndicator <indicator>`
- **Config:** [diff.aIndicator](https://vitest.dev/config/diff#diff-aindicator)

Indicator for expected lines (default: `-`)

<a id="diff-bannotation"></a>
### diff.bAnnotation

- **CLI:** `--diff.bAnnotation <annotation>`
- **Config:** [diff.bAnnotation](https://vitest.dev/config/diff#diff-bannotation)

Annotation for received lines (default: `Received`)

<a id="diff-bindicator"></a>
### diff.bIndicator

- **CLI:** `--diff.bIndicator <indicator>`
- **Config:** [diff.bIndicator](https://vitest.dev/config/diff#diff-bindicator)

Indicator for received lines (default: `+`)

<a id="diff-commonindicator"></a>
### diff.commonIndicator

- **CLI:** `--diff.commonIndicator <indicator>`
- **Config:** [diff.commonIndicator](https://vitest.dev/config/diff#diff-commonindicator)

Indicator for common lines (default: ` `)

<a id="diff-contextlines"></a>
### diff.contextLines

- **CLI:** `--diff.contextLines <lines>`
- **Config:** [diff.contextLines](https://vitest.dev/config/diff#diff-contextlines)

Number of lines of context to show around each change (default: `5`)

<a id="diff-emptyfirstorlastlineplaceholder"></a>
### diff.emptyFirstOrLastLinePlaceholder

- **CLI:** `--diff.emptyFirstOrLastLinePlaceholder <placeholder>`
- **Config:** [diff.emptyFirstOrLastLinePlaceholder](https://vitest.dev/config/diff#diff-emptyfirstorlastlineplaceholder)

Placeholder for an empty first or last line (default: `""`)

<a id="diff-expand"></a>
### diff.expand

- **CLI:** `--diff.expand`
- **Config:** [diff.expand](https://vitest.dev/config/diff#diff-expand)

Expand all common lines (default: `true`)

<a id="diff-includechangecounts"></a>
### diff.includeChangeCounts

- **CLI:** `--diff.includeChangeCounts`
- **Config:** [diff.includeChangeCounts](https://vitest.dev/config/diff#diff-includechangecounts)

Include comparison counts in diff output (default: `false`)

<a id="diff-omitannotationlines"></a>
### diff.omitAnnotationLines

- **CLI:** `--diff.omitAnnotationLines`
- **Config:** [diff.omitAnnotationLines](https://vitest.dev/config/diff#diff-omitannotationlines)

Omit annotation lines from the output (default: `false`)

<a id="diff-printbasicprototype"></a>
### diff.printBasicPrototype

- **CLI:** `--diff.printBasicPrototype`
- **Config:** [diff.printBasicPrototype](https://vitest.dev/config/diff#diff-printbasicprototype)

Print basic prototype Object and Array (default: `true`)

<a id="diff-maxdepth"></a>
### diff.maxDepth

- **CLI:** `--diff.maxDepth <maxDepth>`
- **Config:** [diff.maxDepth](https://vitest.dev/config/diff#diff-maxdepth)

Limit the depth to recurse when printing nested objects (default: `20`)

<a id="diff-truncatethreshold"></a>
### diff.truncateThreshold

- **CLI:** `--diff.truncateThreshold <threshold>`
- **Config:** [diff.truncateThreshold](https://vitest.dev/config/diff#diff-truncatethreshold)

Number of lines to show before and after each change (default: `0`)

<a id="diff-truncateannotation"></a>
### diff.truncateAnnotation

- **CLI:** `--diff.truncateAnnotation <annotation>`
- **Config:** [diff.truncateAnnotation](https://vitest.dev/config/diff#diff-truncateannotation)

Annotation for truncated lines (default: `... Diff result is truncated`)

<a id="exclude"></a>
### exclude

- **CLI:** `--exclude <glob>`
- **Config:** [exclude](https://vitest.dev/config/exclude)

Additional file globs to be excluded from test

<a id="expandsnapshotdiff"></a>
### expandSnapshotDiff

- **CLI:** `--expandSnapshotDiff`
- **Config:** [expandSnapshotDiff](https://vitest.dev/config/expandsnapshotdiff)

Show full diff when snapshot fails

<a id="disableconsoleintercept"></a>
### disableConsoleIntercept

- **CLI:** `--disableConsoleIntercept`
- **Config:** [disableConsoleIntercept](https://vitest.dev/config/disableconsoleintercept)

Disable automatic interception of console logging (default: `false`)

<a id="typecheck-enabled"></a>
### typecheck.enabled

- **CLI:** `--typecheck.enabled`
- **Config:** [typecheck.enabled](https://vitest.dev/config/typecheck#typecheck-enabled)

Enable typechecking alongside tests (default: `false`)

<a id="typecheck-only"></a>
### typecheck.only

- **CLI:** `--typecheck.only`
- **Config:** [typecheck.only](https://vitest.dev/config/typecheck#typecheck-only)

Run only typecheck tests. This automatically enables typecheck (default: `false`)

<a id="typecheck-checker"></a>
### typecheck.checker

- **CLI:** `--typecheck.checker <name>`
- **Config:** [typecheck.checker](https://vitest.dev/config/typecheck#typecheck-checker)

Specify the typechecker to use. Available values are: "tsc" and "vue-tsc" and a path to an executable (default: `"tsc"`)

<a id="typecheck-allowjs"></a>
### typecheck.allowJs

- **CLI:** `--typecheck.allowJs`
- **Config:** [typecheck.allowJs](https://vitest.dev/config/typecheck#typecheck-allowjs)

Allow JavaScript files to be typechecked. By default takes the value from tsconfig.json

<a id="typecheck-ignoresourceerrors"></a>
### typecheck.ignoreSourceErrors

- **CLI:** `--typecheck.ignoreSourceErrors`
- **Config:** [typecheck.ignoreSourceErrors](https://vitest.dev/config/typecheck#typecheck-ignoresourceerrors)

Ignore type errors from source files

<a id="typecheck-tsconfig"></a>
### typecheck.tsconfig

- **CLI:** `--typecheck.tsconfig <path>`
- **Config:** [typecheck.tsconfig](https://vitest.dev/config/typecheck#typecheck-tsconfig)

Path to a custom tsconfig file

<a id="typecheck-spawntimeout"></a>
### typecheck.spawnTimeout

- **CLI:** `--typecheck.spawnTimeout <time>`
- **Config:** [typecheck.spawnTimeout](https://vitest.dev/config/typecheck#typecheck-spawntimeout)

Minimum time in milliseconds it takes to spawn the typechecker

<a id="project"></a>
### project

- **CLI:** `--project <name>`

The name of the project to run if you are using Vitest workspace feature. This can be repeated for multiple projects: `--project=1 --project=2`. You can also filter projects using wildcards like `--project=packages*`, and exclude projects with `--project=!pattern`.

<a id="slowtestthreshold"></a>
### slowTestThreshold

- **CLI:** `--slowTestThreshold <threshold>`
- **Config:** [slowTestThreshold](https://vitest.dev/config/slowtestthreshold)

Threshold in milliseconds for a test or suite to be considered slow (default: `300`)

<a id="teardowntimeout"></a>
### teardownTimeout

- **CLI:** `--teardownTimeout <timeout>`
- **Config:** [teardownTimeout](https://vitest.dev/config/teardowntimeout)

Default timeout of a teardown function in milliseconds (default: `10000`)

<a id="maxconcurrency"></a>
### maxConcurrency

- **CLI:** `--maxConcurrency <number>`
- **Config:** [maxConcurrency](https://vitest.dev/config/maxconcurrency)

Maximum number of concurrent tests and suites during test file execution (default: `5`)

<a id="expect-requireassertions"></a>
### expect.requireAssertions

- **CLI:** `--expect.requireAssertions`
- **Config:** [expect.requireAssertions](https://vitest.dev/config/expect#expect-requireassertions)

Require that all tests have at least one assertion

<a id="expect-poll-interval"></a>
### expect.poll.interval

- **CLI:** `--expect.poll.interval <interval>`
- **Config:** [expect.poll.interval](https://vitest.dev/config/expect#expect-poll-interval)

Poll interval in milliseconds for `expect.poll()` assertions (default: `50`)

<a id="expect-poll-timeout"></a>
### expect.poll.timeout

- **CLI:** `--expect.poll.timeout <timeout>`
- **Config:** [expect.poll.timeout](https://vitest.dev/config/expect#expect-poll-timeout)

Poll timeout in milliseconds for `expect.poll()` assertions (default: `1000`)

<a id="printconsoletrace"></a>
### printConsoleTrace

- **CLI:** `--printConsoleTrace`
- **Config:** [printConsoleTrace](https://vitest.dev/config/printconsoletrace)

Always print console stack traces

<a id="includetasklocation"></a>
### includeTaskLocation

- **CLI:** `--includeTaskLocation`
- **Config:** [includeTaskLocation](https://vitest.dev/config/includetasklocation)

Collect test and suite locations in the `location` property

<a id="attachmentsdir"></a>
### attachmentsDir

- **CLI:** `--attachmentsDir <dir>`
- **Config:** [attachmentsDir](https://vitest.dev/config/attachmentsdir)

The directory where attachments from `context.annotate` are stored in (default: `.vitest-attachments`)

<a id="run"></a>
### run

- **CLI:** `--run`

Disable watch mode

<a id="color"></a>
### color

- **CLI:** `--no-color`

Removes colors from the console output

<a id="clearscreen"></a>
### clearScreen

- **CLI:** `--clearScreen`

Clear terminal screen when re-running tests during watch mode (default: `true`)

<a id="configloader"></a>
### configLoader

- **CLI:** `--configLoader <loader>`

Use `bundle` to bundle the config with esbuild or `runner` (experimental) to process it on the fly. This is only available in vite version 6.1.0 and above. (default: `bundle`)

<a id="standalone"></a>
### standalone

- **CLI:** `--standalone`

Start Vitest without running tests. Tests will be running only on change. If browser mode is enabled, the UI will be opened automatically. This option is ignored when CLI file filters are passed. (default: `false`)

<a id="listtags"></a>
### listTags

- **CLI:** `--listTags [type]`

List all available tags instead of running tests. `--list-tags=json` will output tags in JSON format, unless there are no tags.

<a id="clearcache"></a>
### clearCache

- **CLI:** `--clearCache`

Delete all Vitest caches, including `experimental.fsModuleCache`, without running any tests. This will reduce the performance in the subsequent test run.

<a id="tagsfilter"></a>
### tagsFilter

- **CLI:** `--tagsFilter <expression>`

Run only tests with the specified tags. You can use logical operators `&&` (and), `||` (or) and `!` (not) to create complex expressions, see [Test Tags](https://vitest.dev/guide/test-tags#syntax) for more information.

<a id="stricttags"></a>
### strictTags

- **CLI:** `--strictTags`
- **Config:** [strictTags](https://vitest.dev/config/stricttags)

Should Vitest throw an error if test has a tag that is not defined in the config. (default: `true`)

<a id="experimental-fsmodulecache"></a>
### experimental.fsModuleCache

- **CLI:** `--experimental.fsModuleCache`
- **Config:** [experimental.fsModuleCache](https://vitest.dev/config/experimental#experimental-fsmodulecache)

Enable caching of modules on the file system between reruns.

<a id="experimental-importdurations-print"></a>
### experimental.importDurations.print

- **CLI:** `--experimental.importDurations.print <boolean|on-warn>`
- **Config:** [experimental.importDurations.print](https://vitest.dev/config/experimental#experimental-importdurations-print)

When to print import breakdown to CLI terminal. Use `true` to always print, `false` to never print, or `on-warn` to print only when imports exceed the warn threshold (default: false).

<a id="experimental-importdurations-limit"></a>
### experimental.importDurations.limit

- **CLI:** `--experimental.importDurations.limit <number>`
- **Config:** [experimental.importDurations.limit](https://vitest.dev/config/experimental#experimental-importdurations-limit)

Maximum number of imports to collect and display (default: 0, or 10 if print or UI is enabled).

<a id="experimental-importdurations-failondanger"></a>
### experimental.importDurations.failOnDanger

- **CLI:** `--experimental.importDurations.failOnDanger`
- **Config:** [experimental.importDurations.failOnDanger](https://vitest.dev/config/experimental#experimental-importdurations-failondanger)

Fail the test run if any import exceeds the danger threshold (default: false).

<a id="experimental-importdurations-thresholds-warn"></a>
### experimental.importDurations.thresholds.warn

- **CLI:** `--experimental.importDurations.thresholds.warn <number>`
- **Config:** [experimental.importDurations.thresholds.warn](https://vitest.dev/config/experimental#experimental-importdurations-thresholds-warn)

Warning threshold - imports exceeding this are shown in yellow/orange (default: 100).

<a id="experimental-importdurations-thresholds-danger"></a>
### experimental.importDurations.thresholds.danger

- **CLI:** `--experimental.importDurations.thresholds.danger <number>`
- **Config:** [experimental.importDurations.thresholds.danger](https://vitest.dev/config/experimental#experimental-importdurations-thresholds-danger)

Danger threshold - imports exceeding this are shown in red (default: 500).

<a id="experimental-vitemodulerunner"></a>
### experimental.viteModuleRunner

- **CLI:** `--experimental.viteModuleRunner`
- **Config:** [experimental.viteModuleRunner](https://vitest.dev/config/experimental#experimental-vitemodulerunner)

Control whether Vitest uses Vite's module runner to run the code or fallback to the native `import`. (default: `true`)

<a id="experimental-nodeloader"></a>
### experimental.nodeLoader

- **CLI:** `--experimental.nodeLoader`
- **Config:** [experimental.nodeLoader](https://vitest.dev/config/experimental#experimental-nodeloader)

Controls whether Vitest will use Node.js Loader API to process in-source or mocked files. This has no effect if `viteModuleRunner` is enabled. Disabling this can increase performance. (default: `true`)

<a id="experimental-vcsprovider"></a>
### experimental.vcsProvider

- **CLI:** `--experimental.vcsProvider <path>`
- **Config:** [experimental.vcsProvider](https://vitest.dev/config/experimental#experimental-vcsprovider)

Custom provider for detecting changed files. (default: `git`)

<a id="experimental-preparse"></a>
### experimental.preParse

- **CLI:** `--experimental.preParse`
- **Config:** [experimental.preParse](https://vitest.dev/config/experimental#experimental-preparse)

Parse test specifications before running them. This will apply `.only` flag and test name pattern across all files without running them. (default: `false`)

<a id="changed"></a>
### changed

- **Type:** `boolean | string`
- **Default:** false

Run tests only against changed files. If no value is provided, it will run tests against uncommitted changes (including staged and unstaged).

To run tests against changes made in the last commit, you can use `--changed HEAD~1`. You can also pass commit hash (e.g. `--changed 09a9920`) or branch name (e.g. `--changed origin/develop`).

When used with code coverage the report will contain only the files that were related to the changes.

If paired with the [`forceRerunTriggers`](https://vitest.dev/config/forcereruntriggers) config option it will run the whole test suite if at least one of the files listed in the `forceRerunTriggers` list changes. By default, changes to the Vitest config file and `package.json` will always rerun the whole suite.

<a id="shard"></a>
### shard

- **Type:** `string`
- **Default:** disabled

Test suite shard to execute in a format of `<index>`/`<count>`, where

- `count` is a positive integer, count of divided parts
- `index` is a positive integer, index of divided part

This command will divide all tests into `count` equal parts, and will run only those that happen to be in an `index` part. For example, to split your tests suite into three parts, use this:

```sh
vitest run --shard=1/3
vitest run --shard=2/3
vitest run --shard=3/3
```

**Warning**
You cannot use this option with `--watch` enabled (enabled in dev by default).

**Tip**
If `--reporter=blob` is used without an output file, the default path will include the current shard config to avoid collisions with other Vitest processes.

<a id="merge-reports"></a>
### merge-reports

- **Type:** `boolean | string`

Merges every blob report located in the specified folder (`.vitest-reports` by default). You can use any reporters with this command (except [`blob`](https://vitest.dev/guide/reporters#blob-reporter)):

```sh
vitest --merge-reports --reporter=junit
```
