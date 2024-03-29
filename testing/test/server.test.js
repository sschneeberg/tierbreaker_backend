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

describe('Bracket Routes', function () {
    // POST TEST
    // describe('POST /bracket/create', function () {
    //     it('should build a bracket', function (done) {
    //         const opts = ['one', 'two', 'three', 'four'];
    //         const duration = '2';
    //         const private = true;
    //         request('http://localhost:8000')
    //             .post('/bracket/create')
    //             .send({
    //                 options_list: opts,
    //                 duration: duration,
    //                 title: 'Who would win',
    //                 num_options: opts.length,
    //                 private: private,
    //                 end_display: 'Top'
    //             })
    //             .expect(200)
    //             .expect('Content-Type', /json/)
    //             .then((response) => {
    //                 const bracket = response.body.bracket;
    //                 assert(bracket.num_rounds === Math.log2(opts.length), true);
    //                 assert(bracket.time_duration === parseInt(duration * Math.log2(opts.length)), true);
    //                 assert(bracket.round_duration === parseInt(duration), true);
    //                 assert(bracket.title === 'Who would win', true);
    //                 assert(bracket.end_display_format === 'Top', true);
    //                 assert(bracket.private === private, true);
    //                 for (let i = 0; i < bracket.voting_options.round_options.length; i++) {
    //                     assert(bracket.voting_options.round_options[i] === opts[i], true);
    //                     assert(bracket.voting_options.totals[opts[i]] === 0, true);
    //                     assert(bracket.voting_options.votes[0][opts[i]] === 0, true);
    //                     assert(bracket.voting_options.votes.length === 1, true);
    //                 }
    //                 done();
    //             })
    //             .catch((err) => done(err));
    //     });
    // });
    // GET PUBLIC BRACKETS TEST
    // describe('GET /brackets', function () {
    //     it('should return a 200 status', function (done) {
    //         request('http://localhost:8000').get('/brackets').expect(200, done);
    //     });
    //     it('should return all brackets that are public', function (done) {
    //         request('http://localhost:8000')
    //             .get('/brackets')
    //             .expect('Content-Type', /json/)
    //             .then((response) => {
    //                 const brackets = response.body.public_brackets;
    //                 for (let i = 0; i < brackets.length; i++) {
    //                     assert(brackets[i].private === false, true);
    //                 }
    //                 done();
    //             })
    //             .catch((err) => done(err));
    //     });
    // });
    // GET <bracket_key> TEST
    // describe('GET /brackets/<bracket_key>', function () {
    //     it('should grab a single bracket for the given key', function (done) {
    //         const key = '';
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
    // VOTE TEST
    // describe('PUT /bracket/<bracket_key>/vote', function () {
    //     it('should increment the vote for the proper option by one', function (done) {
    //         const key = '';
    //         const option = 'one';
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
    // EDIT TEST
    // describe('PUT /bracket/<bracket_id>/edit', function () {
    //     it('should change the round and total duration', function (done) {
    //         const id = '';
    //         const title = 'New Who Would Win';
    //         const private = false;
    //     request('http://localhost:8000')
    //             .put(`/bracket/${id}/edit`)
    //             .send({ title: title, private: private })
    //             .expect(200)
    //             .expect('Content-type', /json/)
    //             .then((response) => {
    //                 const bracket = response.body.bracket;
    //                 assert(bracket.time_duration !== originalDurations.total, true);
    //                 assert(bracket.round_duration !== originalDurations.round, true);
    //                 assert(bracket.round_duration === parseInt(duration), true);
    //                 assert(bracket.time_duration === parseInt(duration) * rounds_remaining, true);
    //                 assert(bracket.title === title, true);
    //                 assert(bracket.private === private, true);
    //                 done();
    //             })
    //             .catch((err) => done(err));
    //     });
    // });
    // DELETE TEST
    // describe('DELETE /bracket/<bracket_key>/delete', function () {
    //     it('should delete a bracket', function (done) {
    //         const key = '';
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
    // TALLY TEST
    // describe('PUT /bracket/<bracket_key>/tally', function () {
    //     it('should pick the appropirate winners', function (done) {
    //         const key = ''; //for this key, option "one" should advance, "two" should not, and one of "three" or "four" should
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
