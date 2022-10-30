use itertools::Itertools;

#[allow(dead_code)]
fn main() {
    let number_to_find: u128 = 277777788888899;

    let digits = num_to_digits(number_to_find);

    print_vector(digits);
    println!("{}", digits_to_num(digits));
    return;

    for perm in digits.iter().permutations(digits.len()).unique() {
        let result: Vec<u8> = try_to_find_single_digit_divisors(number_to_find);

        if result.len() > 0 {
            print_vector(result);
        }
    }
}

fn try_to_find_single_digit_divisors(number: u128) -> Vec<u8> {
    if number < 10 {
        return vec![number as u8];
    }

    let mut i = 1u128;
    let max_iteration: u128 = (number as f64).sqrt().ceil() as u128;
    
    while i < max_iteration  {
        i += 1;

        if number % i != 0 {
            continue;
        }

        let mut bag_of_numbers: Vec<u8> = try_to_find_single_digit_divisors(i);
        let other_bag_of_numbers: Vec<u8> = try_to_find_single_digit_divisors(u128::from(number / i));
        bag_of_numbers.extend(other_bag_of_numbers);

        return bag_of_numbers;
    }

    return Vec::<u8>::new();
}

fn digits_to_num(digits: Vec<u8>) -> u128 {
    let mut result: u128 = 0;
    let mut i: u64 = 0;

    for d in digits.iter() {
        result += (d * u128::pow(10, i));
        i += 1;
    }

    return result;
}

fn num_to_digits(num: u128) -> Vec<u8> {
    /*
     * From: https://codereview.stackexchange.com/a/226357 
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
            Some(current)
        }
    })
    .collect::<Vec<u8>>();

    result.reverse();
    result
}

fn print_vector(vector: Vec<u8>) {
    print!("Result!! -> ");
    for v in vector.iter() {
        print!("{}", v);
    }
    println!("");
}