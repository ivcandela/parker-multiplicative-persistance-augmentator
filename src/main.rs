use itertools::Itertools;

enum ParkerSuccess { //Error
    DeadEnd,
}

fn main() {
    let number_to_find: u128 = 277777788888899; // # of unique permutations = 1_261_260

    let digits = num_to_digits(number_to_find);
    let mut permutations_checked = 0u64;
    for perm in digits.iter().permutations(digits.len()).unique() {
        if *perm[0] == 0 {
            continue;
        }
        permutations_checked += 1;
        if permutations_checked % 100 == 0 {
            println!("{}", permutations_checked);
        }

        let current_permutation = digits_to_num(perm);
        
        let result: Vec<u8> = match try_to_find_single_digit_divisors(current_permutation) {
            Ok(ans) => ans,
            Err(_) => Vec::<u8>::new(),
        };

        if result.len() > 0 {
            let mut check: u128 = 1;
            for &d in result.iter() {
                check *= d as u128;
            }

            if check == current_permutation {
                print!("{} -> ", current_permutation);
                print_vector(result);
            }
        }
    }
}

fn try_to_find_single_digit_divisors(number: u128) -> Result<Vec<u8>, ParkerSuccess> {
    if number < 10 {
        return Ok(vec![number as u8]);
    }

    let mut i = 1u128;
    let max_iteration: u128 = (number as f64).sqrt().ceil() as u128;
    
    while i < max_iteration  {
        i += 1;

        if number % i != 0 {
            continue;
        }

        let mut bag_of_numbers: Vec<u8> = try_to_find_single_digit_divisors(i)?;
        let other_bag_of_numbers: Vec<u8> = try_to_find_single_digit_divisors(u128::from(number / i))?;
        bag_of_numbers.extend(other_bag_of_numbers);

        return Ok(bag_of_numbers);
    }

    return Err(ParkerSuccess::DeadEnd);
}

fn digits_to_num(digits: Vec<&u8>) -> u128 {
    let mut result: u128 = 0;
    let mut i: u32 = digits.len().try_into().unwrap();

    for &d in digits.iter() {
        i -= 1;
        result += *d as u128 * 10u128.pow(i);
    }

    return result;
}

fn num_to_digits(num: u128) -> Vec<u8> {
    /*
     * From: https://codereview.stackexchange.com/a/226357 
     *
     * Zero is a special case because
     * it is the terminating value of the unfold below,
     * but given a 0 as input, [0] is expected as output.
     * w/out this check, the output is an empty vec.
     */
    if num == 0 {
        return vec![0];
    }

    let mut x = num;
    let mut result = std::iter::from_fn(move || {
        if x == 0 {
            None
        } else {
            let current = x % 10;
            x /= 10;
            Some(current as u8)
        }
    })
    .collect::<Vec<u8>>();

    result.reverse();
    return result;
}

fn print_vector(vector: Vec<u8>) {
    print!("Result!! -> ");
    for v in vector.iter() {
        print!("{}", v);
    }
    println!("");
}