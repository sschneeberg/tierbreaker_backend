const request = require('supertest');
const assert = require('assert');
const axios = require('axios');

// Note: prior to running tests, all bracket keys must be updated to existing db keys

describe('Server', function () {
    describe('GET /ping', function () {
        it('should return a 200 status', function (done) {
            request('http://localhost:8000').get('/').expect(200, done);
        });
        it('should return pong', function (done) {
            request('http://localhost:8000')
                .get('/')
                .expect('Content-Type', /json/)
                .then((response) => {
                    assert(response.body.ping === 'pong', true);
                    done();
                })
                .catch((err) => done(err));
        });
    });
});

// describe('Bracket Routes', function () {
//     describe('GET /brackets', function () {
//         it('should return a 200 status', function (done) {
//             request('http://localhost:8000').get('/brackets').expect(200, done);
//         });
//         it('should return all brackets that are public', function (done) {
//             request('http://localhost:8000')
//                 .get('/brackets')
//                 .expect('Content-Type', /json/)
//                 .then((response) => {
//                     const brackets = response.body.public_brackets;
//                     for (let i = 0; i < brackets.length; i++) {
//                         assert(brackets[i].private === false, true);
//                     }
//                     done();
//                 })
//                 .catch((err) => done(err));
//         });
//     });

// describe('GET /brackets/<bracket_key>', function () {
//     it('should grab a single bracket for the given key', function (done) {
//         const key = '57000d62';
//         request('http://localhost:8000')
//             .get(`/bracket/${key}`)
//             .expect(200)
//             .expect('Content-Type', /json/)
//             .then((response) => {
//                 const bracket = response.body;
//                 assert(bracket.key === key, true);
//                 done();
//             })
//             .catch((err) => done(err));
//     });
// });

describe('POST /bracket/create', function () {
    it('should build a bracket', function (done) {
        const opts = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight'];
        request('http://localhost:8000')
            .post('/bracket/create')
            .send({
                options_list: opts,
                duration: '4',
                title: 'Who would win ?',
                num_options: '8',
                private: true,
                end_display: 'Winner'
            })
            .expect(200)
            .expect('Content-Type', /json/)
            .then((response) => {
                const bracket = response.body.bracket;
                assert(bracket.num_rounds === Math.log2(8), true);
                assert(bracket.time_duration === 4, true);
                assert(bracket.round_duration === parseInt(4 / Math.log2(8)), true);
                assert(bracket.title === 'Who would win ?', true);
                assert(bracket.end_display_format === 'Winner', true);
                assert(bracket.private === true, true);
                for (let i = 0; i < bracket.voting_options.round_options.length; i++) {
                    assert(bracket.voting_options.round_options[i] === opts[i], true);
                    assert(bracket.voting_options.totals[opts[i]] === 0, true);
                    assert(bracket.voting_options.votes[0][opts[i]] === 0, true);
                    assert(bracket.voting_options.votes.length === 1, true);
                }
                done();
            })
            .catch((err) => done(err));
    });

    // WRITE THIS TEST LATER, NOT VITAL FOR MVP FUNCTIONALITY
    // it('should not have a duplicate key', function () {
    //     const opts = ['one', 'two', 'three', 'four'];
    //     request('http://localhost:8000')
    //         .post('/bracket/create')
    //         .send({
    //             options_list: opts,
    //             duration: '4',
    //             title: 'Who would win 2.0',
    //             num_options: '8',
    //             private: false,
    //             end_display: 'Full'
    //         })
    //         .expect(200)
    //         .expect('Content-Type', /json/)
    //         .then((response) => {
    //             const bracket = response.body.bracket;
    //             assert(bracket.num_rounds === Math.log2(8), true);
    //               // query keys from db and make sure it's not there
    //             done();
    //         })
    //         .catch((err) => done(err));
    // })

    // describe('PUT /bracket/<bracket_key>/vote', function () {
    //     it('should increment the vote for the proper option by one', function (done) {
    //         const key = '57000d62';
    //         const option = 'two';
    //         axios
    //             .get(`http://localhost:8000/bracket/${key}`)
    //             .then((prevVotes) => {
    //                 request('http://localhost:8000')
    //                     .put(`/bracket/${key}/vote`)
    //                     .send({ option: option })
    //                     .expect(200)
    //                     .expect('Content-Type', /json/)
    //                     .then((response) => {
    //                         const bracketVoting = response.body.bracket.voting_options;
    //                         const prevVoting = prevVotes.data.voting_options;
    //                         assert(
    //                             bracketVoting.votes[bracketVoting.votes.length - 1][option] ===
    //                                 prevVoting.votes[prevVoting.votes.length - 1][option] + 1
    //                         );

    //                         assert(bracketVoting.totals[option] === prevVoting.totals[option] + 1);
    //                         done();
    //                     })
    //                     .catch((err) => done(err));
    //             })
    //             .catch((err) => done(err));
    //     });
    // });

    // describe('DELETE /bracket/<bracket_key>/key', function () {
    //     it('should delete a bracket', function (done) {
    //         const key = 'ff7ac740';
    //         request('http://localhost:8000')
    //             .delete(`/bracket/${key}/delete`)
    //             .expect(200)
    //             .then((response) => {
    //                 assert(response.body.msg === 'bracket deleted');
    //                 axios
    //                     .get(`http://localhost:8000/bracket/${key}`)
    //                     .then((response) => {
    //                         assert(response.data.msg === 'no bracket found');
    //                         done();
    //                     })
    //                     .catch((err) => done(err));
    //             })
    //             .catch((err) => done(err));
    //     });
    // });

    // describe('PUt /bracket/<bracket_key>/edit', function () {
    //     it('should change the round and total duration', function (done) {
    //         const key = '6656a5b2';
    //         const duration = '8';
    //         axios
    //             .get(`http://localhost:8000/bracket/${key}`)
    //             .then((original) => {
    //                 const originalDurations = {
    //                     total: original.data.time_duration,
    //                     round: original.data.round_duration
    //                 };
    //                 const rounds_remaining = original.data.num_rounds - original.data.voting_options.votes.length;
    //                 request('http://localhost:8000')
    //                     .put(`/bracket/${key}/edit`)
    //                     .send({ duration: duration })
    //                     .expect(200)
    //                     .expect('Content-type', /json/)
    //                     .then((response) => {
    //                         const bracket = response.body.bracket;
    //                         assert(bracket.time_duration !== originalDurations.total);
    //                         assert(bracket.round_duration !== originalDurations.round);
    //                         assert(bracket.round_duration === parseInt(duration / rounds_remaining));
    //                         done();
    //                     })
    //                     .catch((err) => done(err));
    //             })
    //             .catch((err) => done(err));
    //     });
    // });

    // describe('PUT /bracket/<bracket_key>/tally', function () {
    //     it('should pick the appropirate winners', function (done) {
    //         const key = '57000d62'; //for this key, option "one" should advance, "two" should not, and one of "three" or "four" should
    //         axios
    //             .get(`http://localhost:8000/bracket/${key}`)
    //             .then((original) => {
    //                 const lastRound = original.data.voting_options.round_options;
    //                 request('http://localhost:8000')
    //                     .put(`/bracket/${key}/tally`)
    //                     .expect(200)
    //                     .expect('Content-type', /json/)
    //                     .then((response) => {
    //                         const bracket = response.body.bracket;
    //                         const newRound = bracket.voting_options.round_options;
    //                         const newRoundVotes = bracket.voting_options.votes[bracket.voting_options.votes.length - 1];
    //                         assert(newRound.length === parseInt(lastRound.length / 2));
    //                         assert(newRoundVotes['one'] === 0);
    //                         assert(!newRoundVotes['two']);
    //                         assert(
    //                             (newRoundVotes['three'] === 0 && !newRoundVotes['two']) ||
    //                                 (newRoundVotes['four'] === 0 && !newRoundVotes['three'])
    //                         );
    //                         done();
    //                     })
    //                     .catch((err) => done(err));
    //             })
    //             .catch((err) => done(err));
    //     });
    // });
});
