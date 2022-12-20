use std::env;
use std::fs;
use std::time::Instant;

use hashbrown::HashMap;
use regex::Regex;

#[derive(Debug, Clone)]
struct Bot {
    ore_cost: u16,
    clay_cost: u16,
    obsidian_cost: u16,
}

impl Bot {
    // If this bot can be purchased with the resources we have on hand,
    // do so and return the remainder.
    fn buy(&self, resources: &Resources) -> Option<Resources> {
        if resources.0 >= self.ore_cost
            && resources.1 >= self.clay_cost
            && resources.2 >= self.obsidian_cost
        {
            Some(Resources(
                resources.0 - self.ore_cost,
                resources.1 - self.clay_cost,
                resources.2 - self.obsidian_cost,
                resources.3,
            ))
        } else {
            None
        }
    }
}

#[derive(Debug, Clone)]
struct Blueprint {
    bots: Vec<Bot>,
}

impl Blueprint {
    fn max_costs(&self) -> (u16, u16, u16) {
        (
            self.bots.iter().map(|bot| bot.ore_cost).max().unwrap(),
            self.bots.iter().map(|bot| bot.clay_cost).max().unwrap(),
            self.bots.iter().map(|bot| bot.obsidian_cost).max().unwrap(),
        )
    }
}

#[derive(Debug, Clone, Copy, Hash, Eq, PartialEq)]
struct Bots(u16, u16, u16, u16);

impl Bots {
    fn mine(&self, resources: &mut Resources) {
        resources.0 += self.0;
        resources.1 += self.1;
        resources.2 += self.2;
        resources.3 += self.3;
    }

    fn add(&self, bot: u16) -> Self {
        Self(
            self.0 + if bot == 0 { 1 } else { 0 },
            self.1 + if bot == 1 { 1 } else { 0 },
            self.2 + if bot == 2 { 1 } else { 0 },
            self.3 + if bot == 3 { 1 } else { 0 },
        )
    }
}

#[derive(Debug, Clone, Copy, Hash, Eq, PartialEq)]
struct Resources(u16, u16, u16, u16);

impl Resources {
    fn cap_to_max_costs(&mut self, max_costs: &(u16, u16, u16), bots: &Bots) {
        if self.0 > max_costs.0 && bots.0 >= max_costs.0 {
            self.0 = max_costs.0;
        }
        if self.1 > max_costs.1 && bots.1 >= max_costs.1 {
            self.1 = max_costs.1
        }
        if self.2 > max_costs.2 && bots.2 >= max_costs.2 {
            self.2 = max_costs.2
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = if let Some(_) = args.get(1) {
        "data_test.txt"
    } else {
        "data.txt"
    };
    let re = Regex::new(r"\d+").unwrap();

    let contents = fs::read_to_string(filename).unwrap();
    let mut blueprints = vec![];

    for line in contents.lines() {
        let mut nums = re.captures_iter(line);
        nums.next();
        blueprints.push(Blueprint {
            bots: vec![
                Bot {
                    ore_cost: nums.next().unwrap()[0].parse().unwrap(),
                    clay_cost: 0,
                    obsidian_cost: 0,
                },
                Bot {
                    ore_cost: nums.next().unwrap()[0].parse().unwrap(),
                    clay_cost: 0,
                    obsidian_cost: 0,
                },
                Bot {
                    ore_cost: nums.next().unwrap()[0].parse().unwrap(),
                    clay_cost: nums.next().unwrap()[0].parse().unwrap(),
                    obsidian_cost: 0,
                },
                Bot {
                    ore_cost: nums.next().unwrap()[0].parse().unwrap(),
                    clay_cost: 0,
                    obsidian_cost: nums.next().unwrap()[0].parse().unwrap(),
                },
            ],
        });
    }

    let now = Instant::now();

    println!(
        "Part 1: {}",
        blueprints
            .iter()
            .enumerate()
            .map(|(i, b)| (i + 1) * bf(b, 24))
            .sum::<usize>()
    );

    println!(
        "Part 2: {}",
        blueprints[0..3.min(blueprints.len())]
            .into_iter()
            .map(|b| bf(b, 32))
            .product::<usize>()
    );

    println!("\nDone in {:.2?}", now.elapsed());
}

fn bf(blueprint: &Blueprint, max_time: i32) -> usize {
    let max_costs = blueprint.max_costs();
    let mut cache: HashMap<(i32, Resources, Bots), u16> = HashMap::new();

    fn tick(
        cache: &mut HashMap<(i32, Resources, Bots), u16>,
        blueprint: &Blueprint,
        max_costs: &(u16, u16, u16),
        max_time: i32,
        (time, mut resources, bots): (i32, Resources, Bots),
    ) -> u16 {
        if time >= max_time + 1 {
            return resources.3;
        }
        resources.cap_to_max_costs(max_costs, &bots);
        if let Some(res) = cache.get(&(time, resources, bots)) {
            return res.clone();
        }
        let mut bought = 0;
        let mut best = 0;
        for bot in (0..=3).rev() {
            match bot {
                0 => {
                    if max_costs.0 <= bots.0 {
                        continue;
                    }
                }
                1 => {
                    if max_costs.1 <= bots.1 {
                        continue;
                    }
                }
                2 => {
                    if max_costs.2 <= bots.2 {
                        continue;
                    }
                }
                _ => {}
            }
            if let Some(mut resources_after_spend) = blueprint.bots[bot].buy(&resources) {
                bots.mine(&mut resources_after_spend);
                let next_bots = bots.add(bot as u16);

                let b = tick(
                    cache,
                    &blueprint,
                    &max_costs,
                    max_time,
                    (time + 1, resources_after_spend, next_bots),
                );
                best = best.max(b);
                if time < max_time - 2 {
                    cache.insert((time + 1, resources_after_spend, next_bots), b);
                }
                bought = bot;
                // It would never make sense to not buy the geode bot over the others
                if bot == 3 {
                    break;
                }
            }
        }
        // It would never make sense to not buy the geode bot over buying it
        if bought != 3 {
            bots.mine(&mut resources);

            let b = tick(
                cache,
                &blueprint,
                &max_costs,
                max_time,
                (time + 1, resources, bots),
            );
            best = best.max(b);
            if time < max_time - 2 {
                cache.insert((time + 1, resources, bots), b);
            }
        }
        return best;
    }
    tick(
        &mut cache,
        &blueprint,
        &max_costs,
        max_time,
        (1, Resources(0, 0, 0, 0), Bots(1, 0, 0, 0)),
    ) as usize
}
