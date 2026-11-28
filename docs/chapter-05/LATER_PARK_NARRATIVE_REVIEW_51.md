# Chapter 5 — later-park narrative review 51

**Scope:** structured prose for the new section after the earlier property-return area. The earlier opening and park incidents remain preserved. This is not the complete Chapter 5, a public chapter registration, or a game integration.

The owner selected preservation of the earlier material. Entry below is a proposed connective staging of the approved forward alternatives; the original opening is not replaced.

Each heading names a node in `story/review/chapter-05-later-park/later-park.section.json`. Choices show their next destinations for editorial review. All speech remains in narrative mode; no new portrait artwork is selected.

## later_park_arrival

The path carries you beyond the property-return station.

A supply cable follows a narrow maintenance verge towards a low depot. A worn footpath crosses the grass towards a building with a drinking fountain outside. Farther across the lawn, you can see the refreshments kiosk and a second small brick building.

- TAKE THE FOOTPATH TOWARDS THE DRINKING FOUNTAIN. → fence_arrival
- CROSS THE LAWN TOWARDS THE REFRESHMENTS. → foam_arrival
- FOLLOW THE SUPPLY CABLE TOWARDS THE DEPOT. → depot_early

## fence_arrival

You follow a worn path across the grass. On the other side stands a small park building. You can make out a drinking fountain and two doors.

A metal panel rises behind you.

Then another.

They meet with a solid click.

**Recording:** WELCOME TO THE EXPOSITION'S SELF-ESTABLISHING SECURITY PERIMETER.

Panels begin rising along both sides of the path. Ahead, a final section pushes through the turf, shedding dirt from its pointed top.

**Recording:** INSTALLATION WITHOUT INTERRUPTION TO NORMAL PEDESTRIAN ACTIVITY.

You stop.

Inside the new enclosure, a second row begins to rise.

One section catches on a buried sprinkler pipe. It jerks upward, drops an inch, then tries again. Beneath it, a narrow service cover bangs open with every attempt.

Ahead, there is still a gap.

Above the fence, you can still see the two doors.

- RUN FOR THE REMAINING GAP. → fence_run
- PULL OPEN THE SERVICE COVER BENEATH THE JAMMED SECTION. → fence_release
- CLIMB WHILE THE PANELS ARE STILL LOW. → PASS → fence_climb_success; FAIL → fatal_fence (hidden d6: 3–6 pass, 1–2 fail)

## fence_run

You run.

The final panel rises ahead of you, lifting a rectangle of turf on its pointed top.

You turn sideways and squeeze through.

Behind you, the panel locks into place.

**Recording:** PERIMETER ESTABLISHED IN RECORD TIME.

A small gate opens beside your knee.

An automated mower rolls through it, pauses to let you pass, and continues towards the grass.

The gate closes.

You look from it to the fence.

Then you keep moving towards the park building.

- CONTINUE → first_restroom_approach

## fence_release

You crouch beside the service cover.

Each time the panel tries to rise, the trapped sprinkler pipe bends a little further. Water spurts from a joint, pattering against the underside of the cover.

You pull it open.

Inside is a yellow lever beside a small diagram: pull the lever down, and the fence folds flat.

You pull.

The panel sinks into the ground. You release the lever.

It immediately starts rising again.

**Recording:** MANUAL OVERRIDE ENDED. THANK YOU FOR YOUR ASSISTANCE.

Beyond the lowered section, a narrow concrete channel leads under the fence towards the park building. Water from the broken sprinkler is already running along it.

The lever has a return spring. Beside it is a fixed mounting hook.

- HOLD THE LEVER DOWN AND SQUEEZE THROUGH. → PASS → fence_squeeze_success; FAIL → fatal_fence (hidden d6: 3–6 pass, 1–2 fail)
- USE A RUBBER BAND TO HOLD THE LEVER DOWN. → fence_band; requires {"item": ["rubber_band_ball"]}
- CRAWL ALONG THE DRAINAGE CHANNEL. → fence_drainage

## fence_squeeze_success

You pull the lever down until the panel disappears beneath the grass.

Keeping one hand on it, you step across.

Your fingers slip from the handle.

The machinery starts immediately.

The panel catches the back of your coat.

You wrench forward. A seam gives way, and you stumble onto the path outside.

Behind you, a scrap of fabric rises neatly into position between two steel sections.

**Recording:** PERIMETER INTEGRITY CONFIRMED.

You check yourself. Everything essential appears to have made it.

- CONTINUE → first_restroom_approach

## fence_band

You unwind an outer band from the ball and stretch it between the lever and the mounting hook.

The panel settles beneath the grass.

You cautiously loosen your grip.

It stays down.

You step across.

**Recording:** PERMANENT SECURITY. FLEXIBLE SOLUTIONS.

For once, you agree.

- CONTINUE → first_restroom_approach

## fence_drainage

You lower yourself into the channel. Cold sprinkler water runs into your sleeves.

Halfway through, something brushes your ankle.

It is a leaf.

You continue with considerably more urgency than the leaf warrants.

You climb out beneath an outdoor tap. Your sleeves empty into the channel behind you.

A pair of muddy boots stands beside the back door.

Above the tap hangs a sign.

PLEASE KEEP WATER OFF THE GRASS.

You wring out one cuff over the paving.

The door beside the boots is ajar. Warm air carries the smell of machine oil.

Inside, a control board covers most of one wall. Beneath it stands a large black switch.

PERIMETER MOTOR — RUN / STOP.

You step inside.

- CONTINUE → first_service_room

## fence_climb_success

You plant a shoe on a horizontal rail and pull yourself up.

The panel rises beneath you.

For one encouraging second, it does most of the climbing.

Then the adjoining sections begin moving at different speeds.

You swing a leg over.

Your coat catches on a joint. You pull hard, hear fabric tear, and drop into the planting bed outside.

A shrub beside your head clicks.

You roll away before it finishes turning.

A narrow strip of paving runs between the plants and the park building. You follow it to the open service-room door.

Behind you, the fence announces its completion.

You have already heard enough.

- CONTINUE → first_service_room

## first_restroom_approach

The drinking fountain produces a weak stream of warm water.

You leave it alone.

One door bears a toilet pictogram. Beside its handle, a little green window reads VACANT.

You press the handle.

A bolt clicks inside the frame.

**Recording:** FOR YOUR PROTECTION, PUBLIC FACILITIES WILL UNLOCK WHEN THE SURROUNDING AREA IS SECURE.

Through a narrow window beside the other door, you can see a control board. Rows of green lamps surround one blinking amber square.

A tiny fence diagram identifies the unfinished section.

Somewhere behind you, its motor tries again.

- ENTER THE SERVICE ROOM AND LOOK FOR A MANUAL DOOR RELEASE. → first_service_room
- PRESENT YOUR TEMPORARY STAFF PASS AT THE READER. → first_staff_reader; requires {"item": ["pavilion_temporary_staff_pass"]}
- FOLLOW THE RESTROOM'S DOOR CABLE AROUND THE BUILDING. → first_cable

## first_service_room

Warm air smells of machine oil and freshly cut grass. Through the back window, you can see a lawn mower repeatedly nudging the same fence panel.

The control board covers most of one wall.

A green lamp lights as another section locks into place. The amber square keeps blinking.

Beneath the board is a large black switch:

PERIMETER MOTOR — RUN / STOP.

You turn it to STOP.

The fence motors outside fall silent.

From the other side of the wall comes the welcome sound of a sliding bolt.

You hurry back to the restroom door and press the handle.

- CONTINUE → trapped_occupant

## first_staff_reader

You hold the pass against the reader.

A little roller pulls it halfway into the slot.

**Reader:** HUMAN PRESENTATION.

Inside the building, something clicks.

**Reader:** STAFF ACCESS GRANTED.

The reader returns your pass with a fresh crease across the word TEMPORARY.

You press the door handle.

- CONTINUE → trapped_occupant

## first_cable

The cable runs beneath the window and around the corner of the building.

You follow it to a small exterior box. Its cover hangs open.

Inside, two sockets sit beside a diagram of the door lock. One holds the cable from the fence. The other is marked SERVICE and has a short connecting plug clipped beside it.

You move the plug into the service socket.

The restroom bolt slides back.

Behind you, the fence continues assembling itself.

You return to the door and push.

- CONTINUE → trapped_occupant

## trapped_occupant

The door opens half an inch.

A chain catches.

**Clock-maintenance worker:** Occupied.

You look at the green VACANT window.

**Clock-maintenance worker:** That thing's connected to the fence. I've been in here since they switched it on.

**Player:** I NEED THE BATHROOM.

**Clock-maintenance worker:** So did I. Now I need to get out.

Through the gap, you can see a thick metal brace across the inside of the door. Its upper end has punched through a pipe. Water runs down the wall behind it.

**Clock-maintenance worker:** The fence came up through the floor. Don't switch it back on.

- HELP LIFT THE BRACE SO THE OCCUPANT CAN OPEN THE DOOR. → rescue_brace
- RETURN TO THE CONTROLS AND FIND A WAY TO LOWER THE FENCE. → rescue_retract
- IS THERE ANOTHER TOILET? → other_toilet_directions

## rescue_brace

You put your fingers through the gap beneath the brace.

**Player:** CAN YOU LIFT YOUR END?

**Clock-maintenance worker:** I've been lifting my end.

**Player:** LIFT IT WHEN I LIFT MINE.

A pause.

**Clock-maintenance worker:** All right.

You count to three.

Together, you raise the bar just enough for its lower end to scrape across the floor. The man kicks it sideways.

The door opens.

He steps out quickly, then reaches back to steady the brace against the wall. Water pours from the damaged pipe.

You look inside.

The fence post has split the toilet bowl down the middle.

The man follows your gaze.

**Clock-maintenance worker:** I was hoping that was just the seat.

You let go of the bar.

**Clock-maintenance worker:** There's another building across the lawn. By the refreshments.

He heads towards the service room to find something for the pipe. You take the path towards the lawn.

- CONTINUE → foam_arrival

## rescue_retract

Back in the service room, you find a handwheel beneath the control board. A hinged cover has been hiding it.

MANUAL RETRACTION. TURN UNTIL GROUNDS ARE LEVEL.

You turn.

Outside, the fence descends in short, reluctant jerks. From the restroom comes a scrape, a crash, and a man shouting for you to keep going.

You keep going.

The door opens. A man in an Exposition maintenance jacket steps out, holding his trousers above the spreading water.

**Clock-maintenance worker:** Appreciated.

You look past him.

A steel fence post has split the toilet bowl neatly down the middle.

For a moment, neither of you speaks.

**Clock-maintenance worker:** There's another one across the lawn. By the refreshments.

He notices you looking at his jacket.

**Clock-maintenance worker:** I do the clocks.

He heads towards the service room. You head towards the lawn.

- CONTINUE → foam_arrival

## other_toilet_directions

**Clock-maintenance worker:** Across the lawn. Little building beside the refreshments.

**Player:** DOES IT WORK?

**Clock-maintenance worker:** It did when I went in here.

**Player:** HOW LONG AGO WAS THAT?

His fingers tighten around the edge of the door.

**Clock-maintenance worker:** What time is it?

You decide to keep moving.

- CONTINUE → foam_arrival

## foam_arrival

You can see the refreshments kiosk beyond the grass. Beside it stands a small brick building with a familiar pictogram above the door.

You take the direct route.

**Recording:** PLEASE DISPERSE.

The voice comes from a short post beside the path.

You step aside.

A nozzle beneath the speaker turns to follow you.

**Recording:** PLEASE CONTINUE DISPERSING.

White foam spurts across the paving. It swells into a waist-high barrier, then spreads towards your shoes.

A ribbon of foam slips through a drainage grate beside the path.

You retreat onto the grass.

The nozzle follows.

A metal supply pipe runs from the post to a red valve beside a gardener's service stand. The stand has a little grated platform, currently above the foam.

Along the neighbouring exhibit wall, the mound is growing into a steep white slope. It is almost level with the top.

**Recording:** THANK YOU. CROWD MOVEMENT HAS BEEN DETECTED.

- FOLLOW THE PIPE TO THE RED VALVE. → foam_valve
- CLIMB ONTO THE GARDENER'S STAND. → foam_stand
- USE THE GROWING FOAM TO GET OVER THE NEIGHBOURING WALL. → PASS → foam_climb_success; FAIL → fatal_foam (hidden d6: 3–6 pass, 1–2 fail)

## foam_valve

You follow the pipe, lifting your feet clear of the spreading foam.

The valve is already disappearing beneath a white collar. You grip it with both hands and turn.

The nozzle coughs, spits one final lump, and stops.

The foam keeps growing.

It presses against the gardener's stand, lifting one leg from the ground. Behind it, a maintenance gate bows outward.

The latch snaps.

You squeeze through as the stand tips slowly into the opening.

**Recording:** DISPERSAL COMPLETE. PLEASE VACATE THE DISPERSAL AREA.

Through the bars, you can still see the restroom building. The foam reaches its door handle.

You follow the service path towards a little control hut.

- CONTINUE → control_hut

## foam_stand

You plant one foot on the lower shelf and haul yourself onto the grated platform.

Foam pushes through the holes beneath your shoes.

**Recording:** ELEVATED ATTENDANCE DETECTED.

The nozzle tilts upwards.

You grab the maintenance walkway above you and pull.

A fresh stream strikes the underside of the platform. White foam bulges through the grating, lifting the stand as you scramble onto the walkway.

**Recording:** PLEASE RETURN TO GROUND LEVEL FOR YOUR SAFETY.

Below you, the stand disappears.

The walkway runs above the service path towards a little control hut. Its window is open. A desk fan turns inside, stirring a calendar.

There is nobody at the desk.

- CONTINUE → control_hut

## foam_climb_success

The mound has almost reached the top of the neighbouring exhibit wall.

You press a shoe against its surface.

A thin crust holds your weight. Beneath it, something shifts.

You step up.

The whole mound rises.

For a few seconds, it feels like climbing stairs while someone builds the staircase underneath you.

Then your leading foot breaks through.

You throw yourself forward and catch the top of the wall.

Foam closes around your ankle. Your shoe begins to pull away.

You kick, wrench your leg free, and tumble onto the other side.

A small plaque stands beside a perfectly trimmed hedge.

PLEASE DO NOT ENTER THE EXHIBIT.

You lie beside it until you can breathe properly.

Beyond the hedge is the rear of the control hut. Its back door stands open, giving you a direct way inside.

- CONTINUE → control_hut

## control_hut

*Conditional variant: {"flagIs": ["ch5_later_hut_entry", "front"]}*
From the service path, you enter through the front door.

*Conditional variant: {"flagIs": ["ch5_later_hut_entry", "window"]}*
From the walkway, you climb through the open window.

*Conditional variant: {"flagIs": ["ch5_later_hut_entry", "back"]}*
From the neighbouring exhibit, you come in through the back.

A desk fan blows warm air across a stack of demonstration leaflets.

Behind the desk, a man kneels over an open sample case. He is trying to fit a miniature tree into a compartment slightly too small for it.

**Demonstrator:** Mind the branches. They're live.

You stop moving.

**Player:** ON THE MODEL AS WELL?

**Demonstrator:** Same product. Smaller perimeter.

He gets the lid shut with his knee.

**Player:** I NEED THE BATHROOM.

**Demonstrator:** Brick building by the refreshments.

**Player:** THE FOAM IS COVERING IT.

He looks through the window.

For the first time, his expression changes.

**Demonstrator:** That'll be difficult to get off the brickwork.

He reaches for a telephone, hears something, and puts it down again.

On the wall behind him hangs a large site plan. A narrow path runs behind the restroom building, reached through a staff gate beside the hut.

You point.

**Player:** CAN I GET IN THAT WAY?

**Demonstrator:** Yes. Rear entrance. You'll need the gate open.

He moves a leaflet aside, revealing a brass key.

Then he notices the amber lamps on his control board.

**Demonstrator:** Before anyone goes back out there, I need to get the demonstration under control.

*Conditional variant: {"flagIs": ["ch5_later_foam_discharge", "stopped"]}*
He notices the isolated foam-supply indicator and nods. One system is already stopped.

*Conditional variant: {"flagIs": ["ch5_later_foam_discharge", "running"]}*
Another white bulge rises past the window.

He pulls the remaining leaflets off a large red switch.

- HELP HIM SHUT DOWN THE DEMONSTRATION. → shutdown_help
- SHOW YOUR ACTING DIRECTOR OF VEGETATION CREDENTIAL AND ORDER A SHUTDOWN. → shutdown_director; requires {"item": ["acting_director_badge"]}
- USE YOUR TEMPORARY STAFF PASS TO TAKE THE GATE KEY. → shutdown_staff; requires {"item": ["pavilion_temporary_staff_pass"]}

## shutdown_help

**Player:** WHAT DO YOU NEED ME TO DO?

**Demonstrator:** Watch the grounds. The board says everything's working.

Outside, the foam continues swelling.

You take a position at the open window.

He turns a selector.

**Demonstrator:** Fence?

*Conditional variant: {"flagIs": ["ch5_later_fence", "active"]}*
The rising panels stop.

*Conditional variant: {"flagIs": ["ch5_later_fence", "paused"]}*
The fence panels remain still.

*Conditional variant: {"flagIs": ["ch5_later_fence", "retracted"]}*
The fence remains below ground.

*Conditional variant: {"flagIs": ["ch5_later_fence", "not_triggered"]}*
The fence panels remain flush with the grass.

**Player:** STOPPED.

**Demonstrator:** Dispersal?

*Conditional variant: {"flagIs": ["ch5_later_foam_discharge", "running"]}*
The nozzle droops and releases one final white lump.

*Conditional variant: {"flagIs": ["ch5_later_foam_discharge", "stopped"]}*
The nozzle remains still.

**Player:** STOPPED.

**Demonstrator:** Vegetation?

Along the path, several shrubs sag. A branch unfolds from one, revealing a small glass lens before it goes dark.

The largest tree continues swaying.

**Player:** THAT ONE'S STILL MOVING.

He comes to the window.

**Demonstrator:** That one's a tree.

You wait.

He looks again.

**Demonstrator:** Yes. That's a tree.

He pulls the main switch and hangs a red maintenance tag over it.

Then he takes the brass key and opens the staff gate.

**Demonstrator:** Rear entrance to the toilets. Left at the wall.

You are already through.

- CONTINUE → rear_restroom

## shutdown_director

You place the card on his desk.

He reads it, then looks at the little tree case.

**Demonstrator:** Does that include artificial vegetation?

**Player:** THE APPOINTMENT WAS MADE BY A GARDENING MACHINE.

He considers this.

**Demonstrator:** Then you're probably the right person.

You point to the red switch.

**Player:** SHUT IT ALL DOWN.

He turns a selector from AUTOMATIC to LOCAL, lifts the switch cover, and pulls.

The motors outside fall silent. The nozzle droops. Somewhere nearby, a shrub gives a long electrical whine and falls silent.

The foam already on the lawn continues swelling.

**Demonstrator:** That'll finish expanding. Keep clear of it.

He takes the brass key and opens the staff gate for you.

**Demonstrator:** Anything else, Director?

**Player:** THE BATHROOM.

**Demonstrator:** Right. Yes.

- CONTINUE → rear_restroom

## shutdown_staff

You show him the Temporary Staff Pass.

He glances at the department.

**Demonstrator:** Human Presentation. You people usually want everything running.

You point through the window.

He hands you the key.

**Demonstrator:** Gate, left turn, rear door. I'll deal with this.

As you step outside, you hear him lift the switch cover.

The machinery falls silent. The nozzle sags towards the ground.

You unlock the staff gate and hang the key on a hook just inside, where he told you to leave it.

The path behind the building is narrow but clear.

For several uninterrupted seconds, you simply walk towards a bathroom.

- CONTINUE → rear_restroom

## rear_restroom

The rear door opens.

Inside are a washbasin, a coat hook, and an actual toilet.

You stand very still.

Then a white bubble rises through the bowl.

It grows, trembles, and spills over the rim.

More foam pushes through the floor drain. A little grate lifts on its screws.

You back into the doorway.

The demonstrator appears at the end of the path.

**Demonstrator:** Did it get into the drains?

You look at him.

He starts running towards you.

**Demonstrator:** Don't close the door.

You step outside just as the grate comes free. It lands against the washbasin with a sharp metallic clang.

Behind you, the toilet disappears beneath the foam.

The demonstrator catches up, breathing hard.

**Demonstrator:** Service depot. We need the stripping compound.

He points along the path, towards a low maintenance building beyond the trees.

For the first time since you entered the park, someone else appears to be in a hurry.

- CONTINUE → depot_late

## depot_early

The cable enters the depot through a hole above the door.

Inside, a woman in work overalls has one boot planted on a detached mower head.

**Mechanic:** Public entrance is round the other side.

**Player:** I'M LOOKING FOR A WAY OUT.

She points towards the service lane.

**Mechanic:** Much easier.

When you glance back at the wired shrubs, she takes a foam-release cartridge from the cupboard and offers it to you.

**Mechanic:** One charge. You might want it.

- CONTINUE → depot_offer

## depot_late

You follow him past a row of replacement shrubs hanging from an overhead rail.

Their roots end in electrical plugs.

Beneath one, a shallow tray holds three scorched squirrels.

You give the shrub a wide berth.

The demonstrator shoulders through the depot door.

**Demonstrator:** Foam release. Where is it?

A woman in work overalls looks up from a dismantled lawn mower.

**Mechanic:** Where you left it.

He opens a cupboard and drags out a drum on a little trolley.

You point back towards the restroom.

**Player:** HOW SOON CAN I USE IT?

She looks through the doorway at the white mound rising above the distant roof.

**Mechanic:** Tomorrow.

You stare at her.

**Mechanic:** Afternoon.

The demonstrator wheels the drum away.

The woman reaches into the cupboard and sets a small cartridge on the bench. A broad pictogram shows a spray turning a solid white barrier into a puddle.

**Mechanic:** Pocket applicator. Take it if you're going through the grounds. One charge.

Beside her, the lawn mower's detached cutting head turns towards your shoes.

She puts a boot on it.

**Mechanic:** Stay.

- CONTINUE → depot_offer

## depot_offer

The pocket applicator rests on the bench.

Beyond the depot, a service lane leads towards a pedestrian gate. A yellow line runs through a wide doorway into the dispatch yard.

- TAKE THE FOAM-RELEASE CARTRIDGE. → take_cartridge; requires {"itemNot": ["ch5_foam_release_cartridge"]}
- LEAVE THE CARTRIDGE AND CONTINUE. → depot_departure

## take_cartridge

You pocket the foam-release cartridge.

**Mechanic:** One charge. Point it at the foam.

You look at the dismantled mower beneath her boot.

**Player:** ANYTHING ELSE?

**Mechanic:** Don't let that follow you.

- CONTINUE → depot_departure

## depot_departure

The service lane is open. Inside the dispatch yard, workers move boxed shrubs between storage racks.

- FOLLOW THE SERVICE LANE. → service_gate_exit
- WHERE ARE THOSE BEING INSTALLED? → dispatch_question

## service_gate_exit

You leave.

The service lane passes behind the depot, between stacks of paving slabs and several uprooted trees. Their cables have been coiled neatly around their trunks.

At the end stands an ordinary pedestrian gate.

You lift the latch.

It opens.

You look back.

Nothing rises out of the ground. No speaker addresses you. The gate remains a gate.

You go through before anyone improves it.

Beyond the park, a public footway leads towards the neighbouring buildings. You still urgently need a bathroom.

*Conditional variant: {"item": ["ch5_foam_release_cartridge"]}*
At least you now have something that dissolves one of the things preventing you from reaching one.

**Nonfatal section ending / approved park exit.**


## dispatch_question

**Mechanic:** Along the Exposition boundary. Replacing the old ones.

**Player:** I THOUGHT THEY WERE PROTOTYPES.

She wipes her hands on a rag.

**Mechanic:** That's what the new signs say.

She points you towards the dispatch area.

**Mechanic:** Follow the yellow line. Loading gate comes out beyond the park.

- CONTINUE → dispatch_yard

## dispatch_yard

You pass through a wide doorway into a roofed yard.

Shrubs stand in wooden shipping frames. A worker checks their branches with a voltage probe before another man wraps them in brown paper.

The yellow line runs between the frames.

One crate has been turned sideways. Beneath its fresh delivery label, you can see an older metal plate screwed into the wood.

OFFICE OF UNVERIFIED CONDITIONS.

The return address.

*Conditional variant: {"item": ["expo_examiner_badge", "read"]}*
You recognise the office named on your Temporary Examiner Badge.

You glance into the crate. Its padded compartments hold several empty plant pots, each fitted with a metal socket.

A worker pushes a trolley between you and the crate.

**Dispatch worker:** Mind your feet.

You step aside.

- CONTINUE → dispatch_gate_exit

## dispatch_gate_exit

The loading gate rolls open. Beyond it is the public footway outside the park.

You follow the trolley through.

Behind you, someone calls for another replacement shrub.

**Nonfatal section ending / approved park exit.**


## fatal_fence

Your coat catches between two sections.

You try to lift yourself clear, but there is nowhere left to put your feet.

The machinery keeps rising.

**Recording:** PLEASE STAND CLEAR DURING INSTALLATION.

**Fatal presentation:** PERIMETER COMPLETE

INSTALLATION COMPLETE. NO PERSONNEL REQUIRED.


## fatal_foam

Your leading foot breaks through the crust.

Your other foot follows.

You reach for the wall. Your fingers scrape the stone, then lose it as the mound swells beneath your arms.

The crust closes around your shoulders.

**Recording:** THANK YOU FOR YOUR COOPERATION.

**Fatal presentation:** PLEASE REMAIN DISPERSED

The crust closes around your shoulders. THANK YOU FOR YOUR COOPERATION.
